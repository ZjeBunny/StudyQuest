from pathlib import Path
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QSplitter, QMessageBox, QInputDialog,
    QFileDialog, QDialog, QTextBrowser, QDialogButtonBox, QStackedWidget, QFrame
)
from database.notes_repository import NotesRepository
from services.notes_storage import NotesStorage
from widgets.note.note_editor import NoteEditor
from widgets.note.note_toolbar import NoteToolbar
from widgets.note.note_sidebar import NoteSidebar
from ai.tools import AIWorker


class NotesPage(QWidget):
    page_requested = Signal(str)

    def __init__(self, settings_mng=None):
        super().__init__()
        self.settings_mng = settings_mng
        self.repository = NotesRepository()
        self.storage = NotesStorage()
        self.current_note_id = None
        self.loading_note = False
        self.dirty = False
        self.last_saved_html = None
        self.last_analyzed_html = None
        self.workers = []

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 26, 30, 26)
        root.setSpacing(12)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Notatki")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Twórz i analizuj notatki. Quizy oraz fiszki generuj w zakładce Quizy.")
        subtitle.setObjectName("PageSubtitle")
        title_box.addWidget(title)
        title_box.addWidget(subtitle)
        header.addLayout(title_box)
        header.addStretch()
        self.save_status = QLabel("Wszystkie zmiany zapisane")
        self.save_status.setObjectName("PageSubtitle")
        header.addWidget(self.save_status)
        root.addLayout(header)

        filters = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Szukaj notatek, kategorii lub tagów...")
        self.search.textChanged.connect(self.refresh_notes)
        self.category_filter = QComboBox()
        self.category_filter.currentTextChanged.connect(self.refresh_notes)
        self.category_filter.setMinimumWidth(160)
        self.add_category_button = QPushButton("+ Kategoria")
        self.add_category_button.clicked.connect(self.add_category)
        filters.addWidget(self.search, 1)
        filters.addWidget(self.category_filter)
        filters.addWidget(self.add_category_button)

        self.views = QStackedWidget()
        root.addWidget(self.views, 1)
        browser = QWidget()
        browser_layout = QVBoxLayout(browser)
        browser_layout.setContentsMargins(0, 0, 0, 0)
        browser_layout.setSpacing(12)
        browser_layout.addLayout(filters)
        self.note_sidebar = NoteSidebar()
        self.note_sidebar.note_selected.connect(self.show_note_actions)
        self.note_sidebar.new_note_requested.connect(self.new_note)
        self.note_sidebar.delete_category_requested.connect(self.delete_category)
        self.note_sidebar.rename_category_requested.connect(self.rename_category)
        self.note_sidebar.new_note_in_category_requested.connect(self.new_note)
        browser_layout.addWidget(self.note_sidebar, 1)
        self.views.addWidget(browser)

        actions = QWidget()
        actions_layout = QVBoxLayout(actions)
        actions_layout.setSpacing(16)
        back_actions = QPushButton("← Wszystkie notatki")
        back_actions.clicked.connect(self.show_browser)
        actions_layout.addWidget(back_actions, alignment=Qt.AlignmentFlag.AlignLeft)
        self.selected_note_title = QLabel()
        self.selected_note_title.setObjectName("PageTitle")
        actions_layout.addWidget(self.selected_note_title)
        self.selected_note_category = QLabel()
        self.selected_note_category.setObjectName("PageSubtitle")
        actions_layout.addWidget(self.selected_note_category)
        for label, method, primary in (
            ("✎  Edytuj notatkę", self.edit_selected_note, True),
            ("✓  Wygeneruj quiz", lambda: self.request_quiz("quiz"), False),
            ("▤  Wygeneruj fiszki", lambda: self.request_quiz("flashcards"), False),
            ("🗑  Usuń notatkę", self.delete_note, False),
        ):
            button = QPushButton(label)
            button.setMinimumHeight(52)
            if primary:
                button.setObjectName("PrimaryButton")
            button.clicked.connect(method)
            actions_layout.addWidget(button)
        actions_layout.addStretch(1)
        self.views.addWidget(actions)

        editor_screen = QWidget()
        editor_screen_layout = QVBoxLayout(editor_screen)
        editor_screen_layout.setContentsMargins(0, 0, 0, 0)
        editor_back = QPushButton("← Wróć do notatek")
        editor_back.clicked.connect(self.show_browser)
        editor_screen_layout.addWidget(editor_back, alignment=Qt.AlignmentFlag.AlignLeft)
        self.views.addWidget(editor_screen)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        editor_panel = QWidget()
        editor_layout = QVBoxLayout(editor_panel)
        editor_layout.setContentsMargins(8, 0, 0, 0)
        editor_layout.setSpacing(8)

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Tytuł notatki")
        self.title_input.textChanged.connect(self.mark_dirty)

        meta = QHBoxLayout()
        self.category_input = QComboBox()
        self.category_input.setEditable(True)
        self.category_input.addItem("Bez kategorii")
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Tagi, oddzielone przecinkami")
        meta.addWidget(QLabel("Kategoria"))
        meta.addWidget(self.category_input, 1)
        meta.addWidget(QLabel("Tagi"))
        meta.addWidget(self.tags_input, 2)

        self.editor = NoteEditor()
        self.toolbar = NoteToolbar(self.editor)
        self.editor.textChanged.connect(self.mark_dirty)

        tools_row = QHBoxLayout()
        self.ai_button = QPushButton("AI: analizuj")
        self.ai_button.clicked.connect(self.analyze_now)
        self.pdf_button = QPushButton("Eksport PDF")
        self.pdf_button.clicked.connect(self.export_pdf)
        self.import_button = QPushButton("Importuj PDF/obraz")
        self.import_button.clicked.connect(self.import_source)
        for button in (
            self.ai_button, self.pdf_button, self.import_button
        ):
            tools_row.addWidget(button)
        tools_row.addStretch()

        editor_layout.addWidget(self.title_input)
        editor_layout.addLayout(meta)
        editor_layout.addWidget(self.toolbar)
        editor_layout.addLayout(tools_row)
        editor_layout.addWidget(self.editor, 1)
        editor_screen_layout.addWidget(editor_panel, 1)

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.setInterval(900)
        self.autosave_timer.timeout.connect(self.save_current_note)
        self.title_input.textChanged.connect(self.schedule_save)
        self.tags_input.textChanged.connect(self.schedule_save)
        self.category_input.currentTextChanged.connect(self.schedule_save)

        self.refresh_categories()
        self.refresh_notes()
        self.selected_note_id = None
        self.views.setCurrentIndex(0)

    def ai_config(self):
        base_url = self.settings_mng.get_ollama(
            "base_url", "http://localhost:11434"
        ) if self.settings_mng else "http://localhost:11434"
        model = self.settings_mng.get_ollama(
            "model", "qwen3.5:4b"
        ) if self.settings_mng else "qwen3.5:4b"
        lightweight = self.settings_mng.get("lightweight", False) if self.settings_mng else False
        if lightweight:
            model = self.settings_mng.get_ollama("light_model", "qwen3:1.7b")
        vision = self.settings_mng.get_ollama("vision_model", "gemma3:4b") if self.settings_mng else "gemma3:4b"
        return {"base_url": base_url, "model": model, "vision_model": vision}

    def run_ai(self, operation, *args, success=None):
        worker = AIWorker(operation, *args, **self.ai_config(), parent=self)
        worker.succeeded.connect(
            lambda result, w=worker: self._worker_success(w, result, success)
        )
        worker.failed.connect(
            lambda error, w=worker: self._worker_failed(w, error)
        )
        worker.finished.connect(lambda w=worker: self._forget_worker(w))
        self.workers.append(worker)
        worker.start()

    def _worker_success(self, worker, result, callback):
        if callback:
            callback(result)

    def _worker_failed(self, worker, error):
        self.save_status.setText("AI: wystąpił problem")
        QMessageBox.warning(self, "Asystent AI", error)

    def _forget_worker(self, worker):
        if worker in self.workers:
            self.workers.remove(worker)

    def show_ai_result(self, result, title="Analiza notatki"):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        dialog.resize(760, 600)
        layout = QVBoxLayout(dialog)
        browser = QTextBrowser()
        browser.setOpenExternalLinks(True)
        browser.setMarkdown(str(result))
        layout.addWidget(browser)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(dialog.reject)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)
        dialog.exec()

    def note_text(self):
        return self.editor.toPlainText().strip()

    def mark_dirty(self, *_):
        if not self.loading_note:
            self.dirty = True
            self.save_status.setText("Niezapisane zmiany")
            self.schedule_save()

    def schedule_save(self, *_):
        if not self.loading_note and self.current_note_id:
            self.dirty = True
            self.save_status.setText("Zapisywanie...")
            self.autosave_timer.start()

    def refresh_categories(self):
        current = self.category_filter.currentText()
        editing = self.category_input.currentText() if hasattr(self, "category_input") else ""
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("Wszystkie")
        categories = self.repository.categories()
        self.category_filter.addItems(categories)
        index = self.category_filter.findText(current)
        self.category_filter.setCurrentIndex(max(0, index))
        self.category_filter.blockSignals(False)
        if hasattr(self, "category_input"):
            self.category_input.blockSignals(True)
            self.category_input.clear()
            self.category_input.addItems(categories)
            if editing and editing not in categories:
                self.category_input.addItem(editing)
            self.category_input.setCurrentText(editing or "Bez kategorii")
            self.category_input.blockSignals(False)

    def refresh_notes(self, *_):
        query = self.search.text().strip()
        category = self.category_filter.currentText() or "Wszystkie"
        notes, categories = self.repository.search_notes(query, category)
        self.note_sidebar.set_notes(notes, self.current_note_id, categories)

    def show_browser(self):
        if self.dirty:
            self.save_current_note()
        self.refresh_categories()
        self.refresh_notes()
        self.views.setCurrentIndex(0)

    def show_note_actions(self, note_id):
        if self.dirty:
            self.save_current_note()
        note = self.repository.get(note_id)
        if not note:
            return
        self.selected_note_id = note_id
        self.selected_note_title.setText(note["title"])
        self.selected_note_category.setText("Kategoria: " + note["category"])
        self.views.setCurrentIndex(1)

    def edit_selected_note(self):
        if self.selected_note_id:
            self.open_note(self.selected_note_id)
            self.views.setCurrentIndex(2)

    def request_quiz(self, mode):
        if not self.selected_note_id:
            return
        note = self.repository.get(self.selected_note_id)
        if note:
            self.page_requested.emit("quiz")
            window = self.window()
            quiz = getattr(window, "quiz_page", None)
            if quiz:
                quiz.choose_mode(mode)
                quiz.category.setCurrentIndex(max(0, quiz.category.findData(note["category"])))
                quiz.source.setCurrentIndex(max(0, quiz.source.findData(note["id"])))

    def delete_category(self, category):
        if category == "Bez kategorii":
            QMessageBox.information(self, "Kategoria", "Nie można usunąć kategorii domyślnej.")
            return
        if self.dirty:
            self.save_current_note()
        notes = self.repository.list_notes(category=category)
        answer = QMessageBox.warning(
            self, "Usuń całą kategorię",
            f"Usunąć kategorię „{category}” i wszystkie jej notatki ({len(notes)})?\n"
            "Ta operacja jest nieodwracalna.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.autosave_timer.stop()
        if self.current_note_id in {note["id"] for note in notes}:
            self.current_note_id = None
            self.dirty = False
        for note in notes:
            self.repository.delete(note["id"])
            self.storage.delete(note["content_path"])
        self.repository.remove_category(category)
        self.selected_note_id = None
        self.refresh_categories()
        self.refresh_notes()
        self.views.setCurrentIndex(0)

    def new_note(self, category=None):
        if self.dirty:
            self.save_current_note()
        self.current_note_id = self.storage.new_id()
        self.loading_note = True
        self.title_input.clear()
        self.category_input.setCurrentText(category if isinstance(category, str) and category else "Bez kategorii")
        self.tags_input.clear()
        self.editor.clear()
        self.last_saved_html = None
        self.last_analyzed_html = None
        self.loading_note = False
        self.dirty = True
        self.save_status.setText("Nowa notatka")
        self.views.setCurrentIndex(2)
        self.title_input.setFocus()
        self.autosave_timer.start()

    def open_note(self, note_id):
        if not note_id or note_id == self.current_note_id:
            return
        if self.dirty:
            self.save_current_note()
        note = self.repository.get(note_id)
        if not note:
            return
        self.current_note_id = note_id
        self.loading_note = True
        self.title_input.setText(note["title"])
        self.category_input.setCurrentText(note["category"])
        self.tags_input.setText(", ".join(note["tags"]))
        html = self.storage.load(note["content_path"])
        self.editor.setHtml(html)
        self.last_saved_html = self.editor.toHtml()
        self.last_analyzed_html = None
        self.loading_note = False
        self.dirty = False
        self.save_status.setText("Wszystkie zmiany zapisane")

    def save_current_note(self):
        if not self.current_note_id or not self.dirty:
            return
        title = self.title_input.text().strip() or "Bez tytułu"
        category = self.category_input.currentText().strip() or "Bez kategorii"
        tags = [tag.strip() for tag in self.tags_input.text().split(",") if tag.strip()]
        html = self.editor.toHtml()
        content_changed = html != self.last_saved_html
        existing = self.repository.get(self.current_note_id)
        old_path = existing["content_path"] if existing else None
        path = self.storage.save(self.current_note_id, category, html)
        if existing:
            self.repository.update(self.current_note_id, title, category, path, tags)
            if old_path and old_path != path:
                self.storage.delete(old_path)
        else:
            self.repository.create(self.current_note_id, title, category, path, tags)
        self.last_saved_html = html
        self.dirty = False
        self.save_status.setText("Zapisano")
        self.refresh_categories()
        self.refresh_notes()
    def _analysis_finished(self, result, analyzed_html):
        if analyzed_html == self.editor.toHtml():
            self.save_status.setText("Zapisano · analiza AI gotowa")
            self.show_ai_result(result, "Analiza notatki przez Qwen")
        else:
            self.save_status.setText("Zapisano · analiza starszej wersji pominięta")

    def analyze_now(self):
        if self.dirty:
            self.save_current_note()
        text = self.note_text()
        if not text:
            QMessageBox.information(self, "AI", "Najpierw wpisz treść notatki.")
            return
        self.run_ai(
            "analyze_note", self.title_input.text(), text,
            success=lambda result: self.show_ai_result(result, "Analiza notatki przez Qwen")
        )

    def export_pdf(self):
        if self.dirty:
            self.save_current_note()
        if self.editor.export_pdf(self):
            self.save_status.setText("Wyeksportowano PDF")

    def import_source(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Importuj materiał", "",
            "Materiały (*.pdf *.png *.jpg *.jpeg *.webp *.bmp)"
        )
        if not path:
            return
        if path.lower().endswith(".pdf"):
            operation = "read_pdf"
        else:
            operation = "read_image"
        self.run_ai(
            operation, path,
            success=lambda text: self._insert_imported_text(path, text)
        )

    def _insert_imported_text(self, path, text):
        self.editor.insert_html(
            f"<h2>Import: {Path(path).name}</h2><p>{self._escape_html(text).replace(chr(10), '<br>')}</p>"
        )

    @staticmethod
    def _escape_html(text):
        return (str(text).replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))

    def delete_note(self):
        note_id = self.selected_note_id or self.current_note_id
        if not note_id:
            return
        note = self.repository.get(note_id)
        if not note:
            return
        answer = QMessageBox.question(
            self, "Usuń notatkę", f"Czy na pewno usunąć notatkę „{note['title']}”?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel,
            QMessageBox.StandardButton.Cancel,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.autosave_timer.stop()
        self.repository.delete(note_id)
        self.storage.delete(note["content_path"])
        if self.current_note_id == note_id:
            self.current_note_id = None
            self.dirty = False
        self.selected_note_id = None
        self.refresh_categories()
        self.refresh_notes()
        self.views.setCurrentIndex(0)

    def add_category(self):
        name, accepted = QInputDialog.getText(self, "Nowa kategoria", "Nazwa kategorii:")
        if not accepted:
            return
        name = name.strip()
        if not name:
            QMessageBox.information(self, "Kategoria", "Podaj nazwę kategorii.")
            return
        existing = next((c for c in self.repository.categories() if c.casefold() == name.casefold()), None)
        if existing:
            QMessageBox.information(self, "Kategoria", f"Kategoria „{existing}” już istnieje.")
            self.category_filter.setCurrentText(existing)
            return
        self.repository.add_category(name)
        self.refresh_categories()
        self.category_filter.setCurrentText(name)
        self.refresh_notes()

    def rename_category(self, old_name):
        if old_name == "Bez kategorii":
            QMessageBox.information(self, "Kategoria", "Nie można zmienić nazwy kategorii domyślnej.")
            return
        name, accepted = QInputDialog.getText(
            self, "Zmień nazwę kategorii", "Nowa nazwa:", text=old_name
        )
        if not accepted or not name.strip():
            return
        name = name.strip()
        if name != old_name and any(c.casefold() == name.casefold() for c in self.repository.categories()):
            QMessageBox.warning(self, "Kategoria", "Kategoria o tej nazwie już istnieje.")
            return
        # Save pending edits before moving files to the renamed category.
        if self.dirty:
            self.save_current_note()
        self.repository.rename_category(old_name, name)
        for note in self.repository.list_notes(category=name):
            if note["category"] != name:
                continue
            old_path = note["content_path"]
            html = self.storage.load(old_path)
            new_path = self.storage.save(note["id"], name, html)
            self.repository.update(note["id"], note["title"], name, new_path,
                                   self.repository.get(note["id"])["tags"])
            if old_path != new_path:
                self.storage.delete(old_path)
        if self.current_note_id and self.repository.get(self.current_note_id) and self.repository.get(self.current_note_id)["category"] == name:
            self.category_input.setCurrentText(name)
        self.refresh_categories()
        self.category_filter.setCurrentText(name)
        self.refresh_notes()
