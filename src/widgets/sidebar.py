
from pathlib import Path

from PySide6.QtCore import Qt, Signal, QPropertyAnimation, QEasingCurve
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
        self.icon_label.setFont(QFont(icon_font, 12))
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
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

    def set_compact(self, compact):
        layout = self.layout()

        self.text_label.setVisible(not compact)

        if compact:
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(0)

            layout.setAlignment(
                self.icon_label,
                Qt.AlignmentFlag.AlignCenter
            )

            layout.removeItem(layout.itemAt(2))

        else:
            layout.setContentsMargins(14, 0, 12, 0)
            layout.setSpacing(14)

            layout.addStretch()


class Sidebar(QFrame):
    page_changed = Signal(str)

    def __init__(self, compact=False, animations=True):
        super().__init__()

        self.animations_enabled = animations
        self.expanded_width = 240
        self.compact_width = 68
        self.is_compact = False

        self.setObjectName("Sidebar")
        self.setMinimumWidth(self.expanded_width)
        self.setMaximumWidth(self.expanded_width)

        self.animation = QPropertyAnimation(self, b"maximumWidth")
        self.animation.setDuration(220)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

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

        self.section = QLabel("Mój obszar")
        self.section.setObjectName("SidebarSection")

        layout.addWidget(self.section)
        layout.addSpacing(8)

        navigation = [
            ("\uf015", "Strona główna", "start"),
            ("\uf19d", "Nauka", "study"),
            ("\uf249", "Notatki", "notes"),
            ("\uf0cb", "Quizy", "quiz")
        ]

        for icon, text, key in navigation:
            self.add_navigation_button(
                layout, icon, text, key
            )

        layout.addStretch()

        self.toggle_button = QPushButton("<-")
        self.toggle_button.setObjectName("SidebarToggle")
        self.toggle_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_button.setFont(QFont(self.icon_font, 15))
        self.toggle_button.setFixedHeight(40)
        self.toggle_button.clicked.connect(self.toggle_compact)

        layout.addWidget(self.toggle_button)
        layout.addSpacing(8)

        separator = QFrame()
        separator.setObjectName("SidebarSeparator")
        separator.setFixedHeight(1)

        layout.addWidget(separator)
        layout.addSpacing(8)

        self.add_navigation_button(
            layout, "\uf1de", "Ustawienia", "settings"
        )

        self.select("start")
        if compact:
            self.set_compact(True, animate=False)

    def add_navigation_button(self, layout, icon, text, key):
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

    def select(self, key):
        for name, button in self.buttons.items():
            selected = name == key

            button.setProperty("selected", selected)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def toggle_compact(self):
        self.set_compact(not self.is_compact)

    def set_animations(self, enabled):
        self.animations_enabled = bool(enabled)
        if not self.animations_enabled:
            self.animation.stop()

    def set_compact(self, compact, animate=True):
        self.is_compact = bool(compact)

        target_width = (
            self.compact_width
            if self.is_compact
            else self.expanded_width
        )

        self.animation.stop()

        self.setMinimumWidth(target_width)
        if animate and self.animations_enabled:
            self.animation.setStartValue(self.width())
            self.animation.setEndValue(target_width)
            self.animation.start()
        else:
            self.setMaximumWidth(target_width)

        self.section.setVisible(not self.is_compact)

        for button in self.buttons.values():
            button.set_compact(self.is_compact)

        self.toggle_button.setText(
            "->" if self.is_compact else "<-"
        )
