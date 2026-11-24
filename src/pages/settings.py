from PySide6.QtCore import Qt, Signal, QProcess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QComboBox,
    QCheckBox, QSpinBox, QScrollArea, QPushButton, QMessageBox, QColorDialog
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
    ai_settings_changed = Signal()

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
            ("Jasny", "Light"), ("Ciemny", "Dark"), ("Czarno-zielony", "Green"), ("Czarno-fioletowy", "Purple"), ("Kolorowy", "Kids"), ("Wysoki kontrast", "Contrast")
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
        accent = QPushButton("Wybierz kolor")
        accent.clicked.connect(self.choose_accent)
        section.add_setting("Kolor główny", "Przyciski, ikony i czat", accent)
        reset = QPushButton("Kolor motywu")
        reset.clicked.connect(self.reset_accent)
        section.content.addWidget(reset)
        self.content_layout.addWidget(section)

    def choose_accent(self):
        color = QColorDialog.getColor(parent=self)
        if color.isValid():
            self.settings.set("accent", color.name())
            self.theme_changed.emit(self.theme_combo.currentData())

    def reset_accent(self):
        self.settings.set("accent", "")
        self.theme_changed.emit(self.theme_combo.currentData())

    def create_interface_section(self):
        section = SettingsSection("Interfejs", "Skonfiguruj sposób wyświetlania treści.")
        self.font_size = QSpinBox()
        self.font_size.setRange(10, 24)
        self.font_size.setSuffix(" px")
        self.font_size.setValue(self.settings.get("font_size", 14))
        self.font_size.valueChanged.connect(self.change_font_size)
        section.add_setting(
            "Rozmiar tekstu", "Zmień bazowy rozmiar czcionki aplikacji.",
            self.font_size
        )

        reset_font = QPushButton("Przywróć rozmiar 14 px")
        reset_font.clicked.connect(lambda: self.font_size.setValue(14))
        section.content.addWidget(reset_font)

        self.animations = QCheckBox()
        self.animations.setChecked(self.settings.get("animations", True))
        self.animations.toggled.connect(self.change_animations)
        section.add_setting(
            "Animacje", "Animacja rozwijania i zwijania paska bocznego.",
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
        self.model_combo.addItems(["qwen3.5:4b", "qwen3:4b", "gemma3:4b"])
        self.model_combo.setCurrentText(
            self.settings.get_ollama("model", "qwen3:4b")
        )
        self.model_combo.activated.connect(lambda _: self.change_model(self.model_combo.currentText()))
        self.model_combo.lineEdit().editingFinished.connect(lambda: self.change_model(self.model_combo.currentText()))
        section.add_setting(
            "Model AI", "Nazwa modelu Ollama używanego przez asystenta.",
            self.model_combo
        )

        self.vision_combo = QComboBox()
        self.vision_combo.setEditable(True)
        self.vision_combo.addItem("gemma3:4b")
        self.vision_combo.setCurrentText(self.settings.get_ollama("vision_model", "gemma3:4b"))
        self.vision_combo.activated.connect(lambda _: self.change_vision())
        self.vision_combo.lineEdit().editingFinished.connect(self.change_vision)
        section.add_setting("Model obrazów", "Wybierz model obsługujący obrazy.", self.vision_combo)
        reload_models = QPushButton("Odśwież modele Ollama")
        reload_models.clicked.connect(self.refresh_models)
        section.content.addWidget(reload_models)
        self.lightweight_checkbox = QCheckBox()
        self.lightweight_checkbox.setChecked(self.settings.get("lightweight", False))
        self.lightweight_checkbox.toggled.connect(self.change_lightweight)
        section.add_setting(
            "Tryb Lightweight",
            "Qwen3 1.7B do nauki, notatek, quizów i fiszek. "
            "Analiza obrazów nadal używa Gemma3 4B (1B nie obsługuje obrazów).",
            self.lightweight_checkbox
        )
        self.light_models_info = QLabel("Wymagane modele: qwen3:1.7b; do zdjęć gemma3:4b")
        self.light_models_info.setObjectName("SettingsRowDescription")
        self.light_models_info.setWordWrap(True)
        section.content.addWidget(self.light_models_info)

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
        self.update_active_models()

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

    def update_active_models(self):
        light = self.settings.get("lightweight", False)
        model = self.settings.get_ollama("light_model", "qwen3:1.7b") if light else self.settings.get_ollama("model", "qwen3.5:4b")
        vision = self.settings.get_ollama("vision_model", "gemma3:4b")
        self.light_models_info.setText(f"Tryb: {'Lightweight' if light else 'Normalny'} | Tekst: {model} | Obrazy: {vision}")
        self.model_combo.setEnabled(not light)

    def refresh_models(self):
        import json
        from urllib.request import urlopen
        try:
            with urlopen(self.settings.get_ollama("base_url", "http://localhost:11434").rstrip("/") + "/api/tags", timeout=2) as response:
                names = [m["name"] for m in json.load(response)["models"]]
        except (OSError, ValueError, KeyError) as error:
            self.ollama_status.setText(str(error)); return
        for combo in (self.model_combo, self.vision_combo):
            current = combo.currentText()
            combo.blockSignals(True)
            combo.clear(); combo.addItems(sorted(set(names + [current])))
            combo.setCurrentText(current); combo.blockSignals(False)
        self.ollama_status.setText("Lista modeli odświeżona")

    def change_vision(self):
        self.apply_model(self.vision_combo, "vision_model", "gemma3:4b")

    def change_model(self, value):
        self.apply_model(self.model_combo, "model", "qwen3.5:4b")

    def apply_model(self, combo, key, default):
        value = combo.currentText().strip()
        previous = self.settings.get_ollama(key, default)
        if not value or value == previous:
            return
        def complete(ok):
            if ok: self.settings.set_ollama(key, value)
            combo.setCurrentText(value if ok else previous)
            self.update_active_models(); self.ai_settings_changed.emit()
        self.window().model_setup.ensure([value], complete)

    def change_lightweight(self, enabled):
        if not enabled:
            self.settings.set("lightweight", False)
            self.update_active_models(); self.ai_settings_changed.emit()
            return
        self.lightweight_checkbox.setEnabled(False)
        def complete(ok):
            self.lightweight_checkbox.blockSignals(True)
            self.lightweight_checkbox.setChecked(ok)
            self.lightweight_checkbox.blockSignals(False)
            self.lightweight_checkbox.setEnabled(True)
            self.settings.set("lightweight", ok)
            self.update_active_models(); self.ai_settings_changed.emit()
        self.window().model_setup.ensure([self.settings.get_ollama("light_model", "qwen3:1.7b")], complete)

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
