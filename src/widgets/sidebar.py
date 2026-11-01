
from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)


class NavigationButton(QPushButton):
    def __init__(self, icon, text, key, icon_font):
        super().__init__()

        self.key = key
        self.setObjectName("NavButton")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setProperty("selected", False)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 12, 0)
        layout.setSpacing(14)

        self.icon_label = QLabel(icon)
        self.icon_label.setObjectName("NavIcon")
        self.icon_label.setFont(QFont(icon_font, 15))
        self.icon_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.text_label = QLabel(text)
        self.text_label.setObjectName("NavText")
        self.text_label.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        layout.addWidget(self.icon_label)
        layout.addWidget(self.text_label)
        layout.addStretch()


class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")

        self.buttons = {}

        font_path = (
            Path(__file__).resolve().parents[2]
            / "assets"
            / "fonts"
            / "JetBrainsMonoNerdFont-Regular.ttf"
        )

        font_id = QFontDatabase.addApplicationFont(str(font_path))

        if font_id != -1:
            families = QFontDatabase.applicationFontFamilies(font_id)
            self.icon_font = families[0]
        else:
            self.icon_font = "Segoe UI Symbol"
            print("Warning: Nerd Font could not be loaded.")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 20, 12, 16)
        layout.setSpacing(6)

        section = QLabel("Mój obszar")
        section.setObjectName("SidebarSection")

        layout.addWidget(section)
        layout.addSpacing(8)

        navigation = [
            ("\uf015", "Strona główna", "start"),
            ("\uf19d", "Nauka", "study"),
            ("\uf249", "Notatki", "notes"),
            ("\uf0cb", "Quizy", "quiz")
        ]

        for icon, text, key in navigation:
            button = NavigationButton(
                icon,
                text,
                key,
                self.icon_font
            )

            button.clicked.connect(
                lambda checked=False, k=key: self.page_changed.emit(k)
            )

            layout.addWidget(button)
            self.buttons[key] = button

        layout.addStretch()

        separator = QFrame()
        separator.setObjectName("SidebarSeparator")
        separator.setFixedHeight(1)

        layout.addWidget(separator)
        layout.addSpacing(8)

        settings = NavigationButton(
            "\uf1de",
            "Ustawienia",
            "settings",
            self.icon_font
        )

        settings.clicked.connect(
            lambda: self.page_changed.emit("settings")
        )

        layout.addWidget(settings)
        self.buttons["settings"] = settings

        self.select("start")

    def select(self, key):
        for name, button in self.buttons.items():
            selected = name == key

            button.setProperty("selected", selected)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()
