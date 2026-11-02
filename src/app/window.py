
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QSizePolicy,
    QApplication
)

from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QCursor

from widgets.title_bar import TitleBar
from widgets.sidebar import Sidebar
from pages.start import StartPage
from pages.notes import NotesPage
from pages.quiz import QuizPage
from pages.study import StudyPage
from pages.settings import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self, theme_name):
        super().__init__()
        self.resize_cursor_active = False

        self.resize_margin = 8
        self.setMinimumSize(900, 650)

        self.theme_name = theme_name
        self.setWindowTitle("Study Quest")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.resize(1280, 720)

        self._resize_cursor = None

        main = QWidget()

        ml = QVBoxLayout(main)
        ml.setContentsMargins(0, 0, 0, 0)
        ml.setSpacing(0)

        ml.addWidget(TitleBar(self, theme_name))

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.sidebar = Sidebar()
        self.sidebar.page_changed.connect(self.change_page)

        body.addWidget(self.sidebar, 1)

        self.stack = QStackedWidget()

        self.start_page = StartPage()
        self.start_page.page_requested.connect(self.change_page)
        self.stack.addWidget(self.start_page)

        self.notes_page = NotesPage()
        self.notes_page.page_requested.connect(self.change_page)
        self.stack.addWidget(self.notes_page)

        self.quiz_page = QuizPage()
        self.quiz_page.page_requested.connect(self.change_page)
        self.stack.addWidget(self.quiz_page)

        self.study_page = StudyPage()
        self.study_page.page_requested.connect(self.change_page)
        self.stack.addWidget(self.study_page)

        self.settings_page = SettingsPage()
        self.settings_page.page_requested.connect(self.change_page)
        self.stack.addWidget(self.settings_page)

        self.stack.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )

        body.addWidget(self.stack, 4)

        ml.addLayout(body)
        self.setCentralWidget(main)

        for widget in [self, *self.findChildren(QWidget)]:
            widget.setMouseTracking(True)
            widget.installEventFilter(self)

    def change_page(self, page):
        self.sidebar.select(page)

        match page:
            case "start":
                self.stack.setCurrentWidget(self.start_page)

            case "study":
                self.stack.setCurrentWidget(self.study_page)

            case "notes":
                self.stack.setCurrentWidget(self.notes_page)

            case "quiz":
                self.stack.setCurrentWidget(self.quiz_page)

            case "settings":
                self.stack.setCurrentWidget(self.settings_page)

    def eventFilter(self, watched, event):
        if self.isMaximized() or self.isFullScreen():
            self.reset_resize_cursor()
            return super().eventFilter(watched, event)

        event_type = event.type()

        if event.type() == QEvent.Type.MouseMove:
            position = self.mapFromGlobal(event.globalPosition().toPoint())

            if self.rect().contains(position):
                edges = self.get_resize_edges(position)
                self.update_resize_cursor(edges)
            else:
                self.reset_resize_cursor()

        elif event_type == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                position = self.mapFromGlobal(
                    event.globalPosition().toPoint()
                )

                edges = self.get_resize_edges(position)

                if edges != Qt.Edge(0):
                    self.reset_resize_cursor()

                    window_handle = self.windowHandle()

                    if window_handle:
                        return window_handle.startSystemResize(edges)

        elif event_type == QEvent.Type.Leave:
            if not self.rect().contains(
                self.mapFromGlobal(QCursor.pos())
            ):
                self.reset_resize_cursor()

        return super().eventFilter(watched, event)

    def get_resize_edges(self, position):
        x = position.x()
        y = position.y()

        width = self.width()
        height = self.height()
        margin = self.resize_margin

        edges = Qt.Edge(0)

        if x <= margin:
            edges |= Qt.Edge.LeftEdge
        elif x >= width - margin:
            edges |= Qt.Edge.RightEdge

        if y <= margin:
            edges |= Qt.Edge.TopEdge
        elif y >= height - margin:
            edges |= Qt.Edge.BottomEdge

        return edges

    def update_resize_cursor(self, edges):
        cursors = {
            Qt.Edge.LeftEdge | Qt.Edge.TopEdge: Qt.CursorShape.SizeFDiagCursor,
            Qt.Edge.RightEdge | Qt.Edge.BottomEdge: Qt.CursorShape.SizeFDiagCursor,
            Qt.Edge.RightEdge | Qt.Edge.TopEdge: Qt.CursorShape.SizeBDiagCursor,
            Qt.Edge.LeftEdge | Qt.Edge.BottomEdge: Qt.CursorShape.SizeBDiagCursor,
        }

        if edges in cursors:
            cursor = cursors[edges]
        elif edges & (Qt.Edge.LeftEdge | Qt.Edge.RightEdge):
            cursor = Qt.CursorShape.SizeHorCursor
        elif edges & (Qt.Edge.TopEdge | Qt.Edge.BottomEdge):
            cursor = Qt.CursorShape.SizeVerCursor
        else:
            self.reset_resize_cursor()
            return

        if self.resize_cursor_active:
            QApplication.changeOverrideCursor(QCursor(cursor))
        else:
            QApplication.setOverrideCursor(QCursor(cursor))
            self.resize_cursor_active = True


    def reset_resize_cursor(self):
        if self.resize_cursor_active:
            QApplication.restoreOverrideCursor()
            self.resize_cursor_active = False
