from PySide6.QtCore import Qt, Signal, QProcess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QComboBox,
    QCheckBox, QSpinBox, QScrollArea, QPushButton, QMessageBox
)


class SettingsRow(QFrame):
    def __init__(self, title, description, control):
        super().__init__()
        self.setObjectName("SettingsRow")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(20)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        title_label = QLabel(title)
        title_label.setObjectName("SettingsRowTitle")
        description_label = QLabel(description)
        description_label.setObjectName("SettingsRowDescription")
        description_label.setWordWrap(True)
        text_layout.addWidget(title_label)
        text_layout.addWidget(description_label)
        layout.addLayout(text_layout, 1)
        layout.addWidget(control, 0, Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)


class SettingsSection(QFrame):
    def __init__(self, title, description=""):
        super().__init__()
        self.setObjectName("SettingsSection")
        self.content = QVBoxLayout(self)
        self.content.setContentsMargins(18, 16, 18, 16)
        self.content.setSpacing(8)
        heading = QLabel(title)
        heading.setObjectName("SettingsSectionTitle")
        self.content.addWidget(heading)
        if description:
            subtitle = QLabel(description)
            subtitle.setObjectName("SettingsSectionDescription")
            subtitle.setWordWrap(True)
            self.content.addWidget(subtitle)

    def add_setting(self, title, description, control):
        self.content.addWidget(SettingsRow(title, description, control))


class SettingsPage(QWidget):
    theme_changed = Signal(str)
    font_size_changed = Signal(int)
    animations_changed = Signal(bool)
    sidebar_compact_changed = Signal(bool)
    language_changed = Signal(str)

    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.setObjectName("SettingsPage")
        self.ollama_process = None

        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(20)
        header = QVBoxLayout()
        title = QLabel("Ustawienia")
        title.setObjectName("PageTitle")
        subtitle = QLabel("Dostosuj StudyQuest do swoich potrzeb.")
        subtitle.setObjectName("PageSubtitle")
        header.addWidget(title)
        header.addWidget(subtitle)
        root.addLayout(header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setObjectName("SettingsScrollArea")
        content = QWidget()
        content.setObjectName("SettingsContent")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 8, 0)
        self.content_layout.setSpacing(16)

        self.create_appearance_section()
        self.create_interface_section()
        self.create_ai_section()
        self.create_about_section()
        self.content_layout.addStretch()
        scroll.setWidget(content)
        root.addWidget(scroll, 1)

    def create_appearance_section(self):
        section = SettingsSection("Wygląd", "Dostosuj wygląd aplikacji.")
        self.theme_combo = QComboBox()
        for label, value in (
            ("Systemowy", "System"), ("Ciemny", "Dark"), ("Jasny", "Light")
        ):
            self.theme_combo.addItem(label, value)
        index = self.theme_combo.findData(self.settings.get("theme", "System"))
        self.theme_combo.setCurrentIndex(max(0, index))
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        section.add_setting(
            "Motyw aplikacji",
            "Wybierz jasny, ciemny lub dopasowany do systemu.",
            self.theme_combo
        )
        self.content_layout.addWidget(section)

    def create_interface_section(self):
        section = SettingsSection("Interfejs", "Skonfiguruj sposób wyświetlania treści.")
        self.language_combo = QComboBox()
        self.language_combo.addItem("Polski", "pl")
        self.language_combo.addItem("English", "en")
        self.language_combo.setCurrentIndex(
            max(0, self.language_combo.findData(self.settings.get("language", "pl")))
        )
        self.language_combo.currentIndexChanged.connect(self.change_language)
        section.add_setting(
            "Język", "Zmiana języka zostanie w pełni zastosowana po ponownym uruchomieniu.",
            self.language_combo
        )

        self.font_size = QSpinBox()
        self.font_size.setRange(10, 24)
        self.font_size.setSuffix(" px")
        self.font_size.setValue(self.settings.get("font_size", 14))
        self.font_size.valueChanged.connect(self.change_font_size)
        section.add_setting(
            "Rozmiar tekstu", "Zmień bazowy rozmiar czcionki aplikacji.",
            self.font_size
        )

        self.animations = QCheckBox()
        self.animations.setChecked(self.settings.get("animations", True))
        self.animations.toggled.connect(self.change_animations)
        section.add_setting(
            "Animacje", "Włącz lub wyłącz animacje interfejsu.",
            self.animations
        )

        self.sidebar_compact = QCheckBox()
        self.sidebar_compact.setChecked(self.settings.get("sidebar_compact", False))
        self.sidebar_compact.toggled.connect(self.change_sidebar)
        section.add_setting(
            "Kompaktowy pasek boczny",
            "Pozostaw pasek boczny zwinięty do samych ikon.",
            self.sidebar_compact
        )
        self.content_layout.addWidget(section)

    def create_ai_section(self):
        section = SettingsSection(
            "Sztuczna inteligencja",
            "Konfiguracja lokalnego serwera Ollama."
        )
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.addItems(["qwen3:4b", "qwen3.5:4b", "gemma3:4b"])
        self.model_combo.setCurrentText(
            self.settings.get_ollama("model", "qwen3:4b")
        )
        self.model_combo.currentTextChanged.connect(
            lambda value: self.settings.set_ollama("model", value.strip())
            if value.strip() else None
        )
        section.add_setting(
            "Model AI", "Nazwa modelu Ollama używanego przez asystenta.",
            self.model_combo
        )

        self.auto_start = QCheckBox()
        self.auto_start.setChecked(self.settings.get_ollama("auto_start", True))
        self.auto_start.toggled.connect(
            lambda value: self.settings.set_ollama("auto_start", value)
        )
        section.add_setting(
            "Uruchamianie Ollama",
            "Próbuje uruchomić lokalny serwer Ollama razem z StudyQuest.",
            self.auto_start
        )

        self.test_ollama_button = QPushButton("Sprawdź połączenie")
        self.test_ollama_button.clicked.connect(self.check_ollama)
        self.ollama_status = QLabel("Nie sprawdzono")
        self.ollama_status.setObjectName("SettingsRowDescription")
        row = QHBoxLayout()
        row.addWidget(self.test_ollama_button)
        row.addWidget(self.ollama_status, 1)
        section.content.addLayout(row)
        self.content_layout.addWidget(section)

    def create_about_section(self):
        section = SettingsSection("Informacje", "Informacje o aplikacji.")
        version = QLabel("StudyQuest 1.0.0")
        version.setObjectName("SettingsVersion")
        section.add_setting(
            "Wersja aplikacji", "Aktualnie używana wersja StudyQuest.", version
        )
        reset_button = QPushButton("Przywróć ustawienia domyślne")
        reset_button.clicked.connect(self.reset_settings)
        section.content.addWidget(reset_button)
        self.content_layout.addWidget(section)

    def change_theme(self, index):
        theme = self.theme_combo.itemData(index)
        self.settings.set("theme", theme)
        self.theme_changed.emit(theme)

    def change_language(self, index):
        language = self.language_combo.itemData(index)
        self.settings.set("language", language)
        self.language_changed.emit(language)

    def change_font_size(self, value):
        self.settings.set("font_size", value)
        self.font_size_changed.emit(value)

    def change_animations(self, enabled):
        self.settings.set("animations", enabled)
        self.animations_changed.emit(enabled)

    def change_sidebar(self, compact):
        self.settings.set("sidebar_compact", compact)
        self.sidebar_compact_changed.emit(compact)

    def check_ollama(self):
        self.ollama_status.setText("Sprawdzanie...")
        self.ollama_process = QProcess(self)
        self.ollama_process.finished.connect(self._ollama_finished)
        self.ollama_process.errorOccurred.connect(
            lambda _error: self.ollama_status.setText("Nie znaleziono Ollama")
        )
        self.ollama_process.start("ollama", ["list"])

    def _ollama_finished(self, exit_code, _exit_status):
        if exit_code == 0:
            self.ollama_status.setText("Ollama działa")
        else:
            self.ollama_status.setText("Błąd Ollama")

    def reset_settings(self):
        answer = QMessageBox.question(
            self, "Ustawienia domyślne",
            "Czy przywrócić wszystkie ustawienia domyślne?"
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self.settings.reset()
        QMessageBox.information(
            self, "Ustawienia", "Ustawienia zostały przywrócone. Uruchom aplikację ponownie."
        )
