import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "cutesoc.db"


def initialize_db(db_path=DB_PATH):
    """Create the alerts table if it does not exist."""
    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    severity TEXT NOT NULL,
                    event TEXT NOT NULL,
                    source_ip TEXT NOT NULL,
                    failed_attempts INTEGER NOT NULL,
                    status TEXT NOT NULL
                )
            """)


def save_alert(alert, db_path=DB_PATH):
    """Save an alert only if the same event, IP and severity do not exist."""
    with closing(sqlite3.connect(db_path)) as connection:
        with connection:
            existing = connection.execute("""
                SELECT id
                FROM alerts
                WHERE severity = ?
                  AND event = ?
                  AND source_ip = ?
                ORDER BY id DESC
                LIMIT 1
            """, (
                alert["severity"],
                alert["event"],
                alert["source_ip"],
            )).fetchone()

            if existing is not None:
                return existing[0]

            cursor = connection.execute("""
                INSERT INTO alerts (
                    severity, event, source_ip,
                    failed_attempts, status
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                alert["severity"],
                alert["event"],
                alert["source_ip"],
                alert["failed_attempts"],
                alert["status"],
            ))

            return cursor.lastrowid


def get_alerts(db_path=DB_PATH):
    """Return saved alerts, newest first."""
    with closing(sqlite3.connect(db_path)) as connection:
        connection.row_factory = sqlite3.Row
        with connection:
            rows = connection.execute("""
                SELECT * FROM alerts
                ORDER BY id DESC
            """).fetchall()
            return [dict(row) for row in rows]
