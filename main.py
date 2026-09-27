import sys
import winreg
from PySide6.QtWidgets import QApplication

from src.window import MainWindow
from src.theme import DARK_THEME, LIGHT_THEME

def is_dark_mode():
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
    )
    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
    return value == 0

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("StudyQuest")
    theme = DARK_THEME if is_dark_mode() else LIGHT_THEME
    app.setStyleSheet(theme)

    window = MainWindow(theme)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

