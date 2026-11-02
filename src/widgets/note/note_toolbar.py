
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QPushButton


class NoteToolbar(QFrame):
    def __init__(self, editor):
        super().__init__()

        self.editor = editor

        self.setObjectName("NoteToolbar")

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        actions = [
            (
                "B",
                lambda checked=False: editor.setFontWeight(
                    700 if editor.fontWeight() < 600 else 400
                ),
                "Pogrubienie"
            ),
            (
                "I",
                lambda checked=False: editor.setFontItalic(
                    not editor.fontItalic()
                ),
                "Kursywa"
            ),
            (
                "U",
                lambda checked=False: editor.setFontUnderline(
                    not editor.fontUnderline()
                ),
                "Podkreślenie"
            ),
            (
                "• Lista",
                lambda checked=False: editor.insert_list(),
                "Lista punktowana"
            ),
            (
                "H1",
                lambda checked=False: editor.set_heading(1),
                "Nagłówek 1"
            ),
            (
                "H2",
                lambda checked=False: editor.set_heading(2),
                "Nagłówek 2"
            ),
            (
                "Zwykły tekst",
                lambda checked=False: editor.set_heading(0),
                "Zwykły tekst"
            ),
            (
                "Kolor tekstu",
                lambda checked=False: editor.choose_text_color(),
                "Wybierz kolor tekstu"
            )
        ]

        for label, callback, tooltip in actions:
            button = QPushButton(label)
            button.setToolTip(tooltip)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setFixedHeight(32)
            button.clicked.connect(callback)
            layout.addWidget(button)

        layout.addStretch()
