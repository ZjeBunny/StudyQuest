from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton


class NoteToolbar(QFrame):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setObjectName("NoteToolbar")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        actions = [
            ("B", editor.toggle_bold, "Pogrubienie"),
            ("I", editor.toggle_italic, "Kursywa"),
            ("U", editor.toggle_underline, "Podkreślenie"),
            ("H1", lambda: editor.set_heading(1), "Nagłówek 1"),
            ("H2", lambda: editor.set_heading(2), "Nagłówek 2"),
            ("Tekst", editor.set_normal_text, "Zwykły tekst"),
            ("• Lista", editor.insert_list, "Lista punktowana"),
            ("1. Lista", lambda: editor.insert_list(True), "Lista numerowana"),
            ("Kolor", editor.choose_text_color, "Kolor tekstu"),
            ("Obraz", editor.insert_image, "Wstaw obraz"),
        ]
        for label, callback, tooltip in actions:
            button = QPushButton(label)
            button.setToolTip(tooltip)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFixedHeight(32)
            button.clicked.connect(lambda checked=False, fn=callback: fn())
            layout.addWidget(button)
        layout.addStretch()
