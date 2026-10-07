import sqlite3
from datetime import datetime

DB = "events.db"


def _conn():
    return sqlite3.connect(DB)


def init():
    with _conn() as c:
        c.execute("""CREATE TABLE IF NOT EXISTS events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT, label TEXT, confidence REAL,
            temp REAL, hum REAL, motion INTEGER, alert TEXT)""")


def log_event(label, confidence, sensor, alert):
    s = sensor or {}
    with _conn() as c:
        c.execute("INSERT INTO events(time,label,confidence,temp,hum,motion,alert) VALUES(?,?,?,?,?,?,?)",
                  (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), label, confidence,
                   s.get("temp"), s.get("hum"), s.get("motion"), alert))


def today_events():
    today = datetime.now().strftime("%Y-%m-%d")
    with _conn() as c:
        c.row_factory = sqlite3.Row
        rows = c.execute("SELECT * FROM events WHERE time LIKE ? ORDER BY id", (today + "%",)).fetchall()
    return [dict(r) for r in rows]
