import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from app.window import MainWindow
from services.settings_manager import SettingsManager
from services.ollama_service import OllamaService
from themes.theme import stylesheet, THEMES


def system_theme_is_dark():
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


def resolved_theme(theme_name):
    if theme_name == "System":
        return "Dark" if system_theme_is_dark() else "Light"
    return theme_name if theme_name in THEMES else "Light"


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("StudyQuest")
    app.setOrganizationName("StudyQuest")

    settings = SettingsManager()
    if sys.platform.startswith("linux") and settings.get("theme") == "System":
        settings.set("theme", "Light")
    active_theme = resolved_theme(settings.get("theme", "System"))
    app.setStyleSheet(stylesheet(active_theme, settings.get("accent", ""), settings.get("font_size", 14)))
    font = QFont("Segoe UI")
    font.setPixelSize(settings.get("font_size", 14))
    app.setFont(font)

    if settings.get_ollama("auto_start", True):
        OllamaService(settings.get_ollama(
            "base_url", "http://localhost:11434"
        )).start()

    window = MainWindow(active_theme, settings)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
