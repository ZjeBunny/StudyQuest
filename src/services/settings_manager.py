import json
from copy import deepcopy
from pathlib import Path
from PySide6.QtCore import QStandardPaths


DEFAULT_SETTINGS = {
    "theme": "System",
    "language": "pl",
    "font_size": 14,
    "animations": True,
    "sidebar_compact": False,
    "ollama": {
        "model": "qwen3:4b",
        "auto_start": True,
        "base_url": "http://localhost:11434"
    }
}


class SettingsManager:
    def __init__(self, settings_path=None):
        if settings_path is None:
            base = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppConfigLocation
            )
            self.data_dir = Path(base) / "data"
            # Fallback for environments where Qt returns an empty path.
            if not str(base).strip():
                self.data_dir = Path.home() / ".config" / "StudyQuest" / "data"
            self.settings_file = self.data_dir / "settings.json"
        else:
            self.settings_file = Path(settings_path)
            self.data_dir = self.settings_file.parent

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.settings = self.load()
        self.save()

    def load(self):
        data = deepcopy(DEFAULT_SETTINGS)
        if not self.settings_file.exists():
            return data

        try:
            loaded = json.loads(self.settings_file.read_text(encoding="utf-8"))
            if isinstance(loaded, dict):
                for key, value in loaded.items():
                    if key == "ollama" and isinstance(value, dict):
                        data["ollama"].update(value)
                    elif key in data:
                        data[key] = value
        except (OSError, json.JSONDecodeError):
            # Keep defaults if the settings file is damaged or inaccessible.
            pass

        if data["theme"] not in ("Dark", "Light", "System"):
            data["theme"] = "System"
        if data["language"] not in ("pl", "en"):
            data["language"] = "pl"
        try:
            data["font_size"] = max(10, min(24, int(data["font_size"])))
        except (TypeError, ValueError):
            data["font_size"] = 14
        data["animations"] = bool(data["animations"])
        data["sidebar_compact"] = bool(data["sidebar_compact"])
        return data

    def save(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)
        temporary = self.settings_file.with_suffix(".json.tmp")
        temporary.write_text(
            json.dumps(self.settings, indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        temporary.replace(self.settings_file)

    def get(self, key, default=None):
        return self.settings.get(key, default)

    def set(self, key, value):
        self.settings[key] = value
        self.save()

    def get_ollama(self, key, default=None):
        return self.settings.get("ollama", {}).get(key, default)

    def set_ollama(self, key, value):
        self.settings.setdefault("ollama", {})[key] = value
        self.save()

    def reset(self):
        self.settings = deepcopy(DEFAULT_SETTINGS)
        self.save()
