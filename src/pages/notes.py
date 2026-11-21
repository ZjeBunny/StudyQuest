from pathlib import Path
from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QSplitter, QMessageBox, QInputDialog,
    QFileDialog, QDialog, QTextBrowser, QDialogButtonBox
)
from database.notes_repository import NotesRepository
from services.notes_storage import NotesStorage
from widgets.note.note_editor import NoteEditor
from widgets.note.note_toolbar import NoteToolbar
from widgets.note.note_sidebar import NoteSidebar
from ai.tools import AIWorker


class NotesPage(QWidget):
    page_requested = Signal(str)
    quiz_requested = Signal(str, object)

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
        subtitle = QLabel("Twórz materiały, analizuj je z AI i zamieniaj w questy.")
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
        root.addLayout(filters)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.note_sidebar = NoteSidebar()
        self.note_sidebar.note_selected.connect(self.open_note)
        self.note_sidebar.new_note_requested.connect(self.new_note)
        self.note_sidebar.delete_note_requested.connect(self.delete_note)
        splitter.addWidget(self.note_sidebar)

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
        self.category_input.addItems([
            "Bez kategorii", "Matematyka", "Fizyka", "Chemia", "Informatyka",
            "Języki obce", "Historia", "Biologia"
        ])
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
        self.quiz_button = QPushButton("Utwórz quiz")
        self.quiz_button.clicked.connect(self.create_quiz)
        self.flashcards_button = QPushButton("Fiszki")
        self.flashcards_button.clicked.connect(self.create_flashcards)
        self.pdf_button = QPushButton("Eksport PDF")
        self.pdf_button.clicked.connect(self.export_pdf)
        self.import_button = QPushButton("Importuj PDF/obraz")
        self.import_button.clicked.connect(self.import_source)
        self.web_button = QPushButton("Szukaj w internecie")
        self.web_button.clicked.connect(self.search_web)
        for button in (
            self.ai_button, self.quiz_button, self.flashcards_button,
            self.pdf_button, self.import_button, self.web_button
        ):
            tools_row.addWidget(button)
        tools_row.addStretch()

        editor_layout.addWidget(self.title_input)
        editor_layout.addLayout(meta)
        editor_layout.addWidget(self.toolbar)
        editor_layout.addLayout(tools_row)
        editor_layout.addWidget(self.editor, 1)
        splitter.addWidget(editor_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        root.addWidget(splitter, 1)

        self.autosave_timer = QTimer(self)
        self.autosave_timer.setSingleShot(True)
        self.autosave_timer.setInterval(900)
        self.autosave_timer.timeout.connect(self.save_current_note)
        self.title_input.textChanged.connect(self.schedule_save)
        self.tags_input.textChanged.connect(self.schedule_save)
        self.category_input.currentTextChanged.connect(self.schedule_save)

        self.refresh_categories()
        self.refresh_notes()
        notes = self.repository.list_notes()
        if notes:
            self.open_note(notes[0]["id"])
        else:
            self.new_note()

    def ai_config(self):
        base_url = self.settings_mng.get_ollama(
            "base_url", "http://localhost:11434"
        ) if self.settings_mng else "http://localhost:11434"
        model = self.settings_mng.get_ollama(
            "model", "qwen3.5:4b"
        ) if self.settings_mng else "qwen3.5:4b"
        return {"base_url": base_url, "model": model}

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
        self.category_filter.blockSignals(True)
        self.category_filter.clear()
        self.category_filter.addItem("Wszystkie")
        self.category_filter.addItems(self.repository.categories())
        index = self.category_filter.findText(current)
        self.category_filter.setCurrentIndex(max(0, index))
        self.category_filter.blockSignals(False)

    def refresh_notes(self, *_):
        notes = self.repository.list_notes(
            self.search.text() if hasattr(self, "search") else "",
            self.category_filter.currentText()
            if hasattr(self, "category_filter") and self.category_filter.count()
            else "Wszystkie"
        )
        self.note_sidebar.set_notes(notes, self.current_note_id)

    def new_note(self):
        if self.dirty:
            self.save_current_note()
        self.current_note_id = self.storage.new_id()
        self.loading_note = True
        self.title_input.clear()
        self.category_input.setCurrentText("Bez kategorii")
        self.tags_input.clear()
        self.editor.clear()
        self.last_saved_html = None
        self.last_analyzed_html = None
        self.loading_note = False
        self.dirty = True
        self.save_status.setText("Nowa notatka")
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
        self.save_status.setText("Zapisano · AI analizuje..." if content_changed else "Wszystkie zmiany zapisane")
        self.refresh_categories()
        self.refresh_notes()
        if content_changed and self.note_text():
            self.last_analyzed_html = html
            self.run_ai(
                "analyze_note", title, self.note_text(),
                success=lambda result: self._analysis_finished(result, html)
            )

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

    def create_quiz(self):
        if self.dirty:
            self.save_current_note()
        text = self.note_text()
        if not text:
            QMessageBox.information(self, "Quiz", "Notatka jest pusta.")
            return
        self.quiz_button.setEnabled(False)
        self.run_ai(
            "generate_quiz", self.title_input.text(), text, 8,
            success=self._quiz_ready
        )

    def _quiz_ready(self, questions):
        self.quiz_button.setEnabled(True)
        self.quiz_requested.emit(self.title_input.text() or "Nowy quest", questions)
        self.page_requested.emit("quiz")

    def create_flashcards(self):
        if self.dirty:
            self.save_current_note()
        text = self.note_text()
        if not text:
            QMessageBox.information(self, "Fiszki", "Notatka jest pusta.")
            return
        self.run_ai(
            "generate_flashcards", self.title_input.text(), text, 12,
            success=self._flashcards_ready
        )

    def _flashcards_ready(self, cards):
        lines = []
        for index, card in enumerate(cards, 1):
            lines.append(f"**{index}. {card.get('front', '')}**\n\n{card.get('back', '')}")
        self.show_ai_result("\n\n---\n\n".join(lines), "Fiszki z notatki")

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

    def search_web(self):
        query, accepted = QInputDialog.getText(
            self, "Wyszukiwanie w internecie", "Czego szukać?"
        )
        if not accepted or not query.strip():
            return
        self.run_ai(
            "search_web", query.strip(),
            success=lambda results: self._web_results_ready(query, results)
        )

    def _web_results_ready(self, query, results):
        if not results:
            QMessageBox.information(self, "Wyniki wyszukiwania", "Nie znaleziono wyników.")
            return
        html = "<h2>Wyniki: " + self._escape_html(query) + "</h2>"
        for title, url in results:
            html += (
                '<p><a href="' + self._escape_html(url) + '">'
                + self._escape_html(title) + "</a></p>"
            )
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Wyniki wyszukiwania")
        dialog.setTextFormat(Qt.TextFormat.RichText)
        dialog.setText(html)
        dialog.setInformativeText("Wyniki możesz otworzyć w przeglądarce lub dodać do notatki ręcznie.")
        dialog.exec()

    def delete_note(self):
        if not self.current_note_id:
            return
        note = self.repository.get(self.current_note_id)
        if not note:
            return
        answer = QMessageBox.question(
            self, "Usuń notatkę", "Czy na pewno chcesz usunąć tę notatkę?"
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.autosave_timer.stop()
        self.repository.delete(self.current_note_id)
        self.storage.delete(note["content_path"])
        self.current_note_id = None
        self.dirty = False
        self.refresh_categories()
        self.refresh_notes()
        remaining = self.repository.list_notes()
        if remaining:
            self.open_note(remaining[0]["id"])
        else:
            self.new_note()

    def add_category(self):
        name, accepted = QInputDialog.getText(
            self, "Nowa kategoria", "Nazwa kategorii:"
        )
        if accepted and name.strip():
            self.category_input.setCurrentText(name.strip())
            self.schedule_save()
