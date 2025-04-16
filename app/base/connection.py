from pathlib import Path
from contextlib import contextmanager
import sqlite3

DATABASE_FILE = Path(__file__).parent.parent.parent / "database.db"

@contextmanager
def db_connection():
    with sqlite3.connect(DATABASE_FILE) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        yield conn