from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFrame, QVBoxLayout, QPushButton, QSizePolicy
)

class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 8, 8, 10)

        self.buttons = {}

        for text, key in [
            ("Naucz się", "study"),
            ("Notatki", "notes"),
            ("Quiz", "quiz")
        ]:
            btn = QPushButton(text)
            btn.setObjectName("SidebarBttns")
            btn.clicked.connect(
                lambda _, k=key: self.page_changed.emit(k)
            )

            layout.addWidget(btn)
            self.buttons[key] = btn

        layout.addStretch()

        btn = QPushButton("Ustawienia")
        btn.setObjectName("SidebarBttns")
        btn.clicked.connect(
            lambda: self.page_changed.emit("settings")
        )

        layout.addWidget(btn)
        self.buttons["settings"] = btn

    def select(self, key):
        for name, btn in self.buttons.items():
            btn.setProperty("selected", name == key)
            btn.style().unpolish(btn)
            btn.style().polish(btn)