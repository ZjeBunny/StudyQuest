from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QSizePolicy
)

class SettingsPage(QWidget):
    page_requested = Signal(str)

    def __init__(self):
        super().__init__()
        self.setObjectName("SettingsPage")