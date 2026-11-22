import sys
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QSizePolicy, QApplication, QMessageBox, QMenu, QSystemTrayIcon
)
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QCursor, QFont

from widgets.title_bar import TitleBar
from widgets.sidebar import Sidebar
from pages.start import StartPage
from pages.notes import NotesPage
from pages.quiz import QuizPage
from pages.study import StudyPage
from pages.settings import SettingsPage
from pages.profile import ProfilePage
from datetime import datetime
from themes.theme import DARK_THEME, LIGHT_THEME
from services.ai_status_service import AIStatusService


class MainWindow(QMainWindow):
    def __init__(self, theme_name, settings_mng):
        super().__init__()
        self.settings_mng = settings_mng
        self.theme_name = theme_name
        self.resize_cursor_active = False
        self.resize_margin = 8

        self.setWindowTitle("StudyQuest")
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setMinimumSize(900, 650)
        self.resize(1280, 720)

        central = QWidget()
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = TitleBar(self, theme_name)
        main_layout.addWidget(self.title_bar)

        self.ai_status_service = AIStatusService(
            base_url="http://localhost:11434",
            model=(self.settings_mng.get_ollama("light_model", "qwen3:1.7b")
                   if self.settings_mng.get("lightweight", False)
                   else self.settings_mng.get_ollama("model", "qwen3.5:4b")),
            parent=self
        )

        self.ai_status_service.status_changed.connect(
            self.title_bar.set_ai_status
        )

        self.ai_status_service.start()
        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)

        self.sidebar = Sidebar(
            compact=self.settings_mng.get("sidebar_compact", False),
            animations=self.settings_mng.get("animations", True)
        )
        self.sidebar.page_changed.connect(self.change_page)
        body.addWidget(self.sidebar)

        self.stack = QStackedWidget()
        self.start_page = StartPage()
        self.notes_page = NotesPage(self.settings_mng)
        self.quiz_page = QuizPage(self.settings_mng)
        self.study_page = StudyPage(self.settings_mng)
        self.settings_page = SettingsPage(self.settings_mng)
        self.profile_page = ProfilePage()
        self.settings_page.ai_settings_changed.connect(self.refresh_ai_settings)

        for page in (
            self.start_page, self.notes_page, self.quiz_page,
            self.study_page, self.profile_page, self.settings_page
        ):
            if hasattr(page, "page_requested"):
                page.page_requested.connect(self.change_page)
            self.stack.addWidget(page)

        self.settings_page.theme_changed.connect(self.change_theme)
        self.settings_page.font_size_changed.connect(self.change_font_size)
        self.settings_page.animations_changed.connect(self.sidebar.set_animations)
        self.settings_page.sidebar_compact_changed.connect(self.sidebar.set_compact)
        self.stack.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        body.addWidget(self.stack, 1)
        main_layout.addLayout(body)
        self.setCentralWidget(central)

        self.page_names = {
            "start": "Start", "study": "Nauka", "notes": "Notatki",
            "quiz": "Quizy", "profile": "Moja przygoda", "settings": "Ustawienia"
        }
        self.notifications = []
        self.title_bar.search_requested.connect(self.search_everywhere)
        self.title_bar.notifications_requested.connect(self.show_notifications)
        self.statusBar().hide()  # Bez dodatkowego dolnego paska zajmującego miejsce
        self.quiz_page.activity.connect(self.notify)
        self.study_page.activity.connect(self.notify)
        self.change_page("start")

        for widget in [self, *self.findChildren(QWidget)]:
            widget.setMouseTracking(True)
            widget.installEventFilter(self)

    def change_page(self, page):
        pages = {
            "start": self.start_page, "study": self.study_page,
            "notes": self.notes_page, "quiz": self.quiz_page,
            "profile": self.profile_page,
            "settings": self.settings_page
        }
        if page not in pages:
            return
        self.sidebar.select(page)
        if page in ("quiz", "study"):
            if self.notes_page.dirty:
                self.notes_page.save_current_note()
            if page == "quiz":
                self.quiz_page.refresh_notes()
            else:
                self.study_page.refresh_sources_list()
        if page == "profile":
            self.profile_page.refresh()
        self.stack.setCurrentWidget(pages[page])
        self.title_bar.set_page(self.page_names[page])

    def notify(self, message):
        stamp = datetime.now().strftime("%H:%M")
        self.notifications.insert(0, f"{stamp}  {message}")
        self.notifications = self.notifications[:50]
        self.title_bar.notification_button.setToolTip(f"Powiadomienia ({len(self.notifications)}) — {message}")
        self.statusBar().hide()  # Powiadomienia są dostępne przez ikonę w pasku tytułu

    def show_notifications(self):
        QMessageBox.information(self, "Powiadomienia", "\n\n".join(self.notifications[:12]) if self.notifications else "Brak powiadomień.")

    def search_everywhere(self, query):
        self.change_page("notes")
        self.notes_page.search.setText(query)
        self.notes_page.search.setFocus()
        self.notify(f"Wyszukiwanie notatek: {query}")

    def refresh_ai_settings(self):
        light = self.settings_mng.get("lightweight", False)
        self.ai_status_service.model = (
            self.settings_mng.get_ollama("light_model", "qwen3:1.7b") if light
            else self.settings_mng.get_ollama("model", "qwen3.5:4b")
        )
        self.ai_status_service.base_url = self.settings_mng.get_ollama(
            "base_url", "http://localhost:11434"
        )
        self.title_bar.set_ai_status(False, "Sprawdzanie modelu...")
        self.ai_status_service.check_status()

    def change_theme(self, theme_name):
        self.theme_name = theme_name
        if theme_name == "System":
            theme_name = "Dark" if self._system_theme_is_dark() else "Light"
        QApplication.instance().setStyleSheet(
            DARK_THEME if theme_name == "Dark" else LIGHT_THEME
        )
        self.title_bar.set_theme(theme_name)

    def _system_theme_is_dark(self):
        if sys.platform == "win32":
            try:
                import winreg
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
                ) as key:
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0
            except OSError:
                return False
        return False

    def change_font_size(self, size):
        QApplication.instance().setFont(QFont("Segoe UI", size))

    def eventFilter(self, watched, event):
        if self.isMaximized() or self.isFullScreen():
            self.reset_resize_cursor()
            return super().eventFilter(watched, event)

        event_type = event.type()
        if event_type == QEvent.Type.MouseMove:
            position = self.mapFromGlobal(event.globalPosition().toPoint())
            if self.rect().contains(position):
                self.update_resize_cursor(self.get_resize_edges(position))
            else:
                self.reset_resize_cursor()
        elif event_type == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                position = self.mapFromGlobal(event.globalPosition().toPoint())
                edges = self.get_resize_edges(position)
                if edges != Qt.Edge(0):
                    self.reset_resize_cursor()
                    handle = self.windowHandle()
                    if handle:
                        return handle.startSystemResize(edges)
        elif event_type == QEvent.Type.Leave:
            if not self.rect().contains(self.mapFromGlobal(QCursor.pos())):
                self.reset_resize_cursor()
        return super().eventFilter(watched, event)

    def get_resize_edges(self, position):
        x, y = position.x(), position.y()
        margin = self.resize_margin
        edges = Qt.Edge(0)
        if x <= margin:
            edges |= Qt.Edge.LeftEdge
        elif x >= self.width() - margin:
            edges |= Qt.Edge.RightEdge
        if y <= margin:
            edges |= Qt.Edge.TopEdge
        elif y >= self.height() - margin:
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
