from PySide6.QtWidgets import ( QMainWindow, QWidget,
                                QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy)
from PySide6.QtCore import Qt

from widgets.title_bar import TitleBar
from widgets.sidebar import Sidebar
from pages.start_page import StartPage

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
        self.sidebar=Sidebar()
        self.sidebar.page_changed.connect(self.change_page)
        body.addWidget(self.sidebar, 1); 
        self.stack=QStackedWidget()
        # Undere here goes all pages creating
        self.start_page = StartPage()
        self.start_page.page_requested.connect(self.change_page)
        self.stack.addWidget(self.start_page)
        
        self.stack.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        body.addWidget(self.stack, 4); 
        ml.addLayout(body)
        self.setCentralWidget(main) 

    def change_page(self, page):
        self.sidebar.select(page)

        if page == "start":
            self.stack.setCurrentWidget(self.start_page)
