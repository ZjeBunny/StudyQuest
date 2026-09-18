from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("StudyQuest")
        self.setWindowFlags(Qt.FramelessWindowHint)
        screen_geomety = app.primaryScreen().geometry()
        self.resize(screen_geomety.width(), screen_geomety.height()-25)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        title_bar = QWidget()

        layout.addWidget(title_bar)

        image_label = QLabel()
        image_label.setPixmap(QPixmap("../assets/main_icon.jpg"))

        container.setLayout(layout)
        

        


app = QApplication()

window = MainWindow()
window.show()

app.exec()