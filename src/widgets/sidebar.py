from PySide6.QtCore import Signal
from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton, QLabel

class Sidebar(QFrame):
    page_changed = Signal(str)
    def __init__(self):
        super().__init__()
        self.setObjectName("Sidebar")