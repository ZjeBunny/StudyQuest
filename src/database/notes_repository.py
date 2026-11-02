import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from PySide6.QtCore import QStandardPaths


class NotesRepository:

    def __init__(self, database_path=None):
        if database_path is None:
            base = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
            database_path = Path(base) / "notes.sqlite3"
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def connect(self):
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _initialize(self):
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS notes (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL DEFAULT 'Bez kategorii',
                    content_path TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE
                );
                CREATE TABLE IF NOT EXISTS note_tags (
                    note_id TEXT NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
                    tag_id INTEGER NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
                    PRIMARY KEY(note_id, tag_id)
                );
                CREATE INDEX IF NOT EXISTS idx_notes_updated
                ON notes(updated_at DESC);
                CREATE INDEX IF NOT EXISTS idx_notes_category
                ON notes(category);
            """)
            db.execute(
                "INSERT OR IGNORE INTO notes (id,title,category,content_path,created_at,updated_at) "
                "SELECT '', '', 'Bez kategorii', '', '', '' WHERE 0"
            )

    @staticmethod
    def now():
        return datetime.now(timezone.utc).isoformat(timespec="seconds")

    def create(self, note_id, title, category, content_path, tags=None):
        now = self.now()
        with self.connect() as db:
            db.execute(
                "INSERT INTO notes(id,title,category,content_path,created_at,updated_at) "
                "VALUES(?,?,?,?,?,?)",
                (note_id, title, category, content_path, now, now)
            )
            self._replace_tags(db, note_id, tags or [])

    def update(self, note_id, title, category, content_path, tags=None):
        with self.connect() as db:
            db.execute(
                "UPDATE notes SET title=?, category=?, content_path=?, updated_at=? WHERE id=?",
                (title, category, content_path, self.now(), note_id)
            )
            self._replace_tags(db, note_id, tags or [])

    def _replace_tags(self, db, note_id, tags):
        db.execute("DELETE FROM note_tags WHERE note_id=?", (note_id,))
        for tag in dict.fromkeys(
            item.strip() for item in tags if item.strip()
        ):
            db.execute("INSERT OR IGNORE INTO tags(name) VALUES(?)", (tag,))
            tag_id = db.execute(
                "SELECT id FROM tags WHERE name=?", (tag,)
            ).fetchone()["id"]
            db.execute(
                "INSERT OR IGNORE INTO note_tags(note_id,tag_id) VALUES(?,?)",
                (note_id, tag_id)
            )

    def list_notes(self, query="", category="Wszystkie"):
        sql = """
            SELECT DISTINCT n.*,
                   COALESCE(GROUP_CONCAT(t.name, ', '), '') AS tags
            FROM notes n
            LEFT JOIN note_tags nt ON nt.note_id=n.id
            LEFT JOIN tags t ON t.id=nt.tag_id
            WHERE 1=1
        """
        args = []
        if query.strip():
            sql += " AND (n.title LIKE ? OR n.category LIKE ? OR t.name LIKE ?)"
            pattern = f"%{query.strip()}%"
            args.extend([pattern, pattern, pattern])
        if category != "Wszystkie":
            sql += " AND n.category=?"
            args.append(category)
        sql += " GROUP BY n.id ORDER BY n.updated_at DESC"
        with self.connect() as db:
            return [dict(row) for row in db.execute(sql, args).fetchall()]

    def get(self, note_id):
        with self.connect() as db:
            row = db.execute(
                "SELECT * FROM notes WHERE id=?", (note_id,)
            ).fetchone()
            if not row:
                return None
            result = dict(row)
            tags = db.execute(
                "SELECT t.name FROM tags t JOIN note_tags nt ON nt.tag_id=t.id "
                "WHERE nt.note_id=? ORDER BY t.name",
                (note_id,)
            ).fetchall()
            result["tags"] = [item["name"] for item in tags]
            return result

    def categories(self):
        with self.connect() as db:
            rows = db.execute(
                "SELECT DISTINCT category FROM notes ORDER BY category"
            ).fetchall()
            return [row["category"] for row in rows]

    def delete(self, note_id):
        with self.connect() as db:
            db.execute("DELETE FROM notes WHERE id=?", (note_id,))
