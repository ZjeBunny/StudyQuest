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
        layout.setContentsMargins(16, 4, 16, 4)

        image = QLabel()
        image.setPixmap(QPixmap("assets/light_mode_main.jpg" if self.theme == LIGHT_THEME else "assets/dark_mode_main.png"))
        image.setFixedSize(32, 32)
        image.setScaledContents(True)
        layout.addWidget(image)

        title = QLabel("StudyQuest")
        title.setStyleSheet("font-size:20px;font-weight:700;")
        layout.addWidget(title)

        layout.addStretch()

        self.minizmize = QPushButton("🗕"); self.minizmize.setFixedSize(24, 24); self.minizmize.setObjectName("minimizeapp")
        self.maximize = QPushButton("🗖"); self.maximize.setFixedSize(24, 24); self.maximize.setObjectName("maximizeapp")
        self.exitapp = QPushButton("✖"); self.exitapp.setFixedSize(24, 24); self.exitapp.setObjectName("exitapp")

        layout.addWidget(self.minizmize); layout.addWidget(self.maximize); layout.addWidget(self.exitapp)

        self.minizmize.clicked.connect(window.showMinimized)
        self.maximize.clicked.connect(self.tog_maximize)
        self.exitapp.clicked.connect(window.close)

        self.drag = None

        self.setLayout(layout)

    def tog_maximize(self):
        self.window.showNormal() if self.window.isMaximized() else self.window.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag and event.buttons() & Qt.LeftButton:
            current = event.globalPosition().toPoint()
            self.window.move(self.window.pos() + current - self.drag)
            self.drag = current 

    def mouseReleaseEvent(self, event):
        self.drag = None

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.tog_maximize()