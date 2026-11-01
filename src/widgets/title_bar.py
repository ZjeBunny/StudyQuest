
from PySide6.QtCore import Qt, Signal, QPoint
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit
)
from PySide6.QtGui import QPixmap
from pathlib import Path

class TitleBar(QFrame):
    search_requested = Signal(str)
    notifications_requested = Signal()

    def __init__(self, window, theme_name):
        super().__init__()

        self.theme_name = theme_name
        self.window = window
        self.drag_position = None

        self.setObjectName("TitleBar")
        self.setFixedHeight(52)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 0, 8, 0)
        layout.setSpacing(10)

        self.logo = QLabel()
        self.logo.setObjectName("TitleLogo")
        logo_path = Path(__file__).resolve().parents[2] / "assets" / "images"

        if theme_name == "Dark":
            pixmap = QPixmap(str(logo_path / "dark_logo.png"))
        else:
            pixmap = QPixmap(str(logo_path / "light_logo.png"))

        if not pixmap.isNull():
            self.logo.setPixmap(
                pixmap.scaled(
                    30,
                    30,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        self.logo.setFixedSize(34, 34)
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("StudyQuest")
        self.title.setObjectName("TitleText")

        self.separator = QLabel("/")
        self.separator.setObjectName("TitleSeparator")

        self.current_page = QLabel("Start")
        self.current_page.setObjectName("CurrentPage")

        layout.addWidget(self.logo)
        layout.addWidget(self.title)
        layout.addWidget(self.separator)
        layout.addWidget(self.current_page)

        layout.addStretch()

        self.ai_status = QLabel("● AI Offline")
        self.ai_status.setObjectName("AIStatus")
        self.set_ai_status(False)

        layout.addWidget(self.ai_status)

        self.search_input = QLineEdit()
        self.search_input.setObjectName("TitleSearch")
        self.search_input.setPlaceholderText("Szukaj...")
        self.search_input.setFixedWidth(200)
        self.search_input.setClearButtonEnabled(True)
        self.search_input.hide()
        self.search_input.returnPressed.connect(self.emit_search)

        layout.addWidget(self.search_input)

        self.search_button = QPushButton("⌕")
        self.search_button.setObjectName("TitleButton")
        self.search_button.setToolTip("Wyszukaj")
        self.search_button.clicked.connect(self.toggle_search)

        layout.addWidget(self.search_button)

        self.notification_button = QPushButton("♧")
        self.notification_button.setObjectName("TitleButton")
        self.notification_button.setToolTip("Powiadomienia")
        self.notification_button.clicked.connect(
            self.notifications_requested.emit
        )

        layout.addWidget(self.notification_button)

        self.separator_line = QFrame()
        self.separator_line.setObjectName("TitleLine")
        self.separator_line.setFixedSize(1, 24)

        layout.addWidget(self.separator_line)

        self.minimize_button = QPushButton("—")
        self.minimize_button.setObjectName("WindowButton")
        self.minimize_button.clicked.connect(self.window.showMinimized)

        self.maximize_button = QPushButton("□")
        self.maximize_button.setObjectName("WindowButton")
        self.maximize_button.clicked.connect(self.toggle_maximize)

        self.close_button = QPushButton("×")
        self.close_button.setObjectName("CloseButton")
        self.close_button.clicked.connect(self.window.close)

        layout.addWidget(self.minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(self.close_button)

    def set_page(self, name):
        self.current_page.setText(name)

    def set_ai_status(self, online):
        if online:
            self.ai_status.setText("● AI Online")
            self.ai_status.setStyleSheet(
                "color: #65C98A; font-size: 11px; padding: 0 8px;"
            )
        else:
            self.ai_status.setText("● AI Offline")
            self.ai_status.setStyleSheet(
                "color: #E47777; font-size: 11px; padding: 0 8px;"
            )

    def toggle_search(self):
        visible = self.search_input.isVisible()
        self.search_input.setVisible(not visible)

        if not visible:
            self.search_input.setFocus()
        else:
            self.search_input.clear()

    def emit_search(self):
        query = self.search_input.text().strip()

        if query:
            self.search_requested.emit(query)

    def toggle_maximize(self):
        if self.window.isMaximized():
            self.window.showNormal()
            self.maximize_button.setText("□")
        else:
            self.window.showMaximized()
            self.maximize_button.setText("❐")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.window.frameGeometry().topLeft()
            )

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (
            self.drag_position is not None
            and event.buttons() & Qt.MouseButton.LeftButton
            and not self.window.isMaximized()
        ):
            self.window.move(
                event.globalPosition().toPoint()
                - self.drag_position
            )

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_position = None
        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.toggle_maximize()

        super().mouseDoubleClickEvent(event)
