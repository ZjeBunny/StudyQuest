from pathlib import Path
from uuid import uuid4
from PySide6.QtCore import QStandardPaths


class NotesStorage:
    """Stores note HTML files separately from the SQLite metadata database."""

    def __init__(self, notes_dir=None):
        if notes_dir is None:
            base = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
            notes_dir = Path(base) / "notes"
        self.root = Path(notes_dir)
        self.root.mkdir(parents=True, exist_ok=True)

    def _safe_category(self, category):
        value = "".join(
            char.lower() if char.isalnum() else "-"
            for char in (category or "Bez kategorii").strip()
        ).strip("-")
        return value or "bez-kategorii"

    def path_for(self, note_id, category):
        folder = self.root / self._safe_category(category)
        folder.mkdir(parents=True, exist_ok=True)
        return folder / f"{note_id}.html"

    def save(self, note_id, category, html):
        path = self.path_for(note_id, category)
        temporary = path.with_suffix(".html.tmp")
        temporary.write_text(html or "", encoding="utf-8")
        temporary.replace(path)
        return str(path)

    def load(self, path):
        file_path = Path(path)
        if not file_path.exists():
            return ""
        return file_path.read_text(encoding="utf-8")

    def delete(self, path):
        if path:
            try:
                Path(path).unlink(missing_ok=True)
            except OSError:
                pass

    @staticmethod
    def new_id():
        return uuid4().hex
