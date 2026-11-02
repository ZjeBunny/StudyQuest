from PySide6.QtCore import Qt, Signal, QTimer
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QSplitter, QMessageBox, QInputDialog
)
from database.notes_repository import NotesRepository
from services.notes_storage import NotesStorage
from widgets.note.note_editor import NoteEditor
from widgets.note.note_toolbar import NoteToolbar
from widgets.note.note_sidebar import NoteSidebar


class NotesPage(QWidget):
    page_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("NotesPage")
        self.repository = NotesRepository()
        self.storage = NotesStorage()
        self.current_note_id = None
        self.loading_note = False
        self.dirty = False

        root = QVBoxLayout(self)
        root.setContentsMargins(30, 26, 30, 26)
        root.setSpacing(14)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        title = QLabel("Notatki")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Twórz, porządkuj i zapisuj swoje materiały.")
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
        self.category_input.addItems(["Bez kategorii", "Matematyka", "Fizyka", "Chemia", "Informatyka"])
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText("Tagi, oddzielone przecinkami")
        meta.addWidget(QLabel("Kategoria"))
        meta.addWidget(self.category_input, 1)
        meta.addWidget(QLabel("Tagi"))
        meta.addWidget(self.tags_input, 2)

        self.editor = NoteEditor()
        self.toolbar = NoteToolbar(self.editor)
        self.editor.textChanged.connect(self.mark_dirty)

        editor_layout.addWidget(self.title_input)
        editor_layout.addLayout(meta)
        editor_layout.addWidget(self.toolbar)
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
        self.editor.setHtml(self.storage.load(note["content_path"]))
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
        existing = self.repository.get(self.current_note_id)
        old_path = existing["content_path"] if existing else None
        path = self.storage.save(self.current_note_id, category, html)
        if existing:
            self.repository.update(
                self.current_note_id, title, category, path, tags
            )
            if old_path and old_path != path:
                self.storage.delete(old_path)
        else:
            self.repository.create(
                self.current_note_id, title, category, path, tags
            )
        self.dirty = False
        self.save_status.setText("Wszystkie zmiany zapisane")
        self.refresh_categories()
        self.refresh_notes()

    def delete_note(self):
        if not self.current_note_id:
            return
        note = self.repository.get(self.current_note_id)
        if not note:
            return
        answer = QMessageBox.question(
            self, "Usuń notatkę",
            "Czy na pewno chcesz usunąć tę notatkę?"
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
