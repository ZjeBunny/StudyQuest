from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QLabel, QPushButton


class NoteSidebar(QWidget):
    note_selected = Signal(str)
    new_note_requested = Signal()
    delete_note_requested = Signal()

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        heading = QLabel("Twoje notatki")
        heading.setObjectName("SectionTitle")
        layout.addWidget(heading)

        self.list = QListWidget()
        self.list.currentItemChanged.connect(self._selected)
        layout.addWidget(self.list, 1)

        buttons = QVBoxLayout()
        self.new_button = QPushButton("+ Nowa notatka")
        self.new_button.setObjectName("PrimaryButton")
        self.new_button.clicked.connect(self.new_note_requested)
        self.delete_button = QPushButton("Usuń notatkę")
        self.delete_button.clicked.connect(self.delete_note_requested)
        buttons.addWidget(self.new_button)
        buttons.addWidget(self.delete_button)
        layout.addLayout(buttons)

    def _selected(self, current, previous):
        if current:
            self.note_selected.emit(current.data(256))

    def set_notes(self, notes, selected_id=None):
        from PySide6.QtWidgets import QListWidgetItem
        self.list.blockSignals(True)
        self.list.clear()
        selected = None
        for note in notes:
            item = QListWidgetItem(note["title"] or "Bez tytułu")
            item.setData(256, note["id"])
            item.setToolTip(
                f'{note["category"]}\n{note.get("tags", "")}'
            )
            self.list.addItem(item)
            if note["id"] == selected_id:
                selected = item
        if selected:
            self.list.setCurrentItem(selected)
        self.list.blockSignals(False)
