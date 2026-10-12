import tempfile
import unittest
from pathlib import Path

from database.db import initialize_db, save_alert, get_alerts


class TestAlertDatabase(unittest.TestCase):

    def test_save_and_retrieve_alert(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_cutesoc.db"
            initialize_db(db_path)

            alert = {
                "severity": "HIGH",
                "event": "Multiple failed login attempts",
                "source_ip": "192.0.2.10",
                "failed_attempts": 3,
                "status": "Suspicious activity detected",
            }

            alert_id = save_alert(alert, db_path)
            saved_alerts = get_alerts(db_path)

            self.assertEqual(len(saved_alerts), 1)
            self.assertEqual(saved_alerts[0]["id"], alert_id)
            self.assertEqual(saved_alerts[0]["source_ip"], "192.0.2.10")
            self.assertEqual(saved_alerts[0]["failed_attempts"], 3)
            self.assertEqual(saved_alerts[0]["severity"], "HIGH")

    def test_initialize_database_twice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_cutesoc.db"

            initialize_db(db_path)
            initialize_db(db_path)

            self.assertEqual(get_alerts(db_path), [])

    def test_duplicate_alert_is_not_saved_twice(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = Path(temp_dir) / "test_cutesoc.db"
            initialize_db(db_path)

            alert = {
                "severity": "HIGH",
                "event": "Multiple failed login attempts",
                "source_ip": "192.0.2.10",
                "failed_attempts": 3,
                "status": "Suspicious activity detected",
            }

            first_id = save_alert(alert, db_path)
            second_id = save_alert(alert, db_path)

            saved_alerts = get_alerts(db_path)

            self.assertEqual(first_id, second_id)
            self.assertEqual(len(saved_alerts), 1)


if __name__ == "__main__":
    unittest.main()
