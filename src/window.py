from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("StudyQuest")
        #self.setWindowFlags(Qt.FramelessWindowHint)

        label = QLabel("Hello Study Quest")
        label.setAlignment(Qt.AlignCenter)

        self.setCentralWidget(label)

app = QApplication()

window = MainWindow()
window.show()

app.exec()