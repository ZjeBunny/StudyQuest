from PySide6.QtWidgets import (QApplication, QMainWindow, QLabel, QWidget,
                                QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy)
from PySide6.QtCore import Qt

from src.widgets.title_bar import TitleBar
from src.widgets.sidebar import Sidebar

class MainWindow(QMainWindow):

    def __init__(self, theme_name):
        super().__init__()
        self.theme_name = theme_name
        self.setWindowTitle("Study Quest")
        self.setWindowFlag(Qt.FramelessWindowHint); self.resize(1280 , 720)
        main = QWidget()
        ml = QVBoxLayout(main); ml.setContentsMargins(0,0,0,0); ml.setSpacing(0)
        ml.addWidget(TitleBar(self, theme_name))
        body=QHBoxLayout(); 
        body.setContentsMargins(0,0,0,0); body.setSpacing(0);        
        self.sidebar=Sidebar(); body.addWidget(self.sidebar, 1); 
        self.stack=QStackedWidget()
        self.stack.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        body.addWidget(self.stack, 4); 
        ml.addLayout(body)
        self.setCentralWidget(main) 
