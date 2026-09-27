from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt

from src.widgets.title_bar import TitleBar
from src.widgets.sidebar import Sidebar

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Study Quest")
        self.setWindowFlag(Qt.FramelessWindowHint); self.resize(1280 , 720)
        main = QWidget()
        ml = QVBoxLayout(main); ml.setContentsMargins(0,0,0,0); ml.setSpacing(0)
        ml.addWidget(TitleBar(self))
        body=QHBoxLayout(); 
        body.setContentsMargins(0,0,0,0); body.setSpacing(0);        
        self.sidebar=Sidebar(); body.addWidget(self.sidebar); 
        self.stack=QStackedWidget()
        body.addWidget(self.stack); 
        ml.addLayout(body)
        self.setCentralWidget(main)
