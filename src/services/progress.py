"""Local SQLite study statistics; no internet connection."""
import sqlite3
from datetime import datetime, timezone
from database.notes_repository import NotesRepository

class ProgressStore:
    def __init__(self):
        self.notes = NotesRepository()
        with self.notes.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS study_stats (id INTEGER PRIMARY KEY CHECK(id=1), correct INTEGER NOT NULL DEFAULT 0, incorrect INTEGER NOT NULL DEFAULT 0, seconds INTEGER NOT NULL DEFAULT 0, generated INTEGER NOT NULL DEFAULT 0)")
            db.execute("INSERT OR IGNORE INTO study_stats(id) VALUES(1)")
    def record(self, correct=0, incorrect=0, seconds=0, generated=0):
        with self.notes.connect() as db:
            db.execute("UPDATE study_stats SET correct=correct+?, incorrect=incorrect+?, seconds=seconds+?, generated=generated+? WHERE id=1", (correct,incorrect,max(0,int(seconds)),generated))
    def snapshot(self):
        with self.notes.connect() as db:
            data=dict(db.execute("SELECT * FROM study_stats WHERE id=1").fetchone())
            data['notes']=db.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        data['xp']=data['correct']*10 + data['generated']*5
        level=1; remaining=data['xp']; threshold=100
        while remaining>=threshold:
            remaining-=threshold;level+=1;threshold=100+50*(level-1)
        data.update(level=level, progress=remaining, next_xp=threshold, badges=[f"Poziom {n} • Odznaka odkrywcy" for n in range(2,level+1)])
        return data
