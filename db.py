import sqlite3
from contextlib import contextmanager

DB = "history.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT, competency TEXT, q_type TEXT,
                answer TEXT, overall INTEGER, ts DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def save_attempt(q, answer, fb):
    with get_db() as c:
        c.execute(
            "INSERT INTO attempts (question, competency, q_type, answer, overall) "
            "VALUES (?, ?, ?, ?, ?)",
            (q["text"], q["competency"], q["type"], answer, fb["overall"]),
        )

def weak_areas():
    with get_db() as c:
        rows = c.execute(
            "SELECT competency, AVG(overall) avg_score, COUNT(*) n "
            "FROM attempts GROUP BY competency ORDER BY avg_score ASC"
        ).fetchall()
    return [dict(r) for r in rows]
