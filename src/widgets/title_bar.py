from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton
from PySide6.QtGui import QPixmap

from src.theme import LIGHT_THEME

class TitleBar(QFrame):
    def __init__(self, window, theme):
        super().__init__()
        self.theme = theme
        self.window = window
        self.setObjectName("TitleBar")
        self.setFixedHeight(40)

        layout = QHBoxLayout()
        layout.setContentsMargins(16, 8, 16, 8)

        image = QLabel()
        image.setPixmap(QPixmap("assets/light_mode_main.jpg" if self.theme == LIGHT_THEME else "assets/dark_mode_main.png"))
        image.setFixedSize(24, 24)
        image.setScaledContents(True)
        layout.addWidget(image)

        title = QLabel("StudyQuest")
        title.setStyleSheet("font-size:16px;font-weight:700;")
        layout.addWidget(title)

        layout.addStretch()

        self.setLayout(layout)