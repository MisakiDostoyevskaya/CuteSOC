
import unittest

from analyzer.detection_rules import detect_brute_force


class TestBruteForceDetection(unittest.TestCase):

    def test_detects_three_failed_logins(self):
        logs = [
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["severity"], "HIGH")
        self.assertEqual(alerts[0]["source_ip"], "192.0.2.10")
        self.assertEqual(alerts[0]["failed_attempts"], 3)

    def test_two_failed_logins_do_not_trigger_alert(self):
        logs = [
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(alerts, [])

    def test_successful_logins_do_not_trigger_alert(self):
        logs = [
            {"event_type": "login_success", "source_ip": "192.0.2.10"},
            {"event_type": "login_success", "source_ip": "192.0.2.10"},
            {"event_type": "login_success", "source_ip": "192.0.2.10"},
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(alerts, [])


    def test_detects_multiple_source_ips(self):
        logs = [
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
            {"event_type": "login_failed", "source_ip": "192.0.2.10"},
            {"event_type": "login_failed", "source_ip": "198.51.100.7"},
            {"event_type": "login_failed", "source_ip": "198.51.100.7"},
            {"event_type": "login_failed", "source_ip": "198.51.100.7"},
        ]

        alerts = detect_brute_force(logs)

        self.assertEqual(len(alerts), 2)
        self.assertEqual(
            {alert["source_ip"] for alert in alerts},
            {"192.0.2.10", "198.51.100.7"},
        )

    def test_empty_logs_return_no_alerts(self):
        alerts = detect_brute_force([])

        self.assertEqual(alerts, [])


if __name__ == "__main__":
    unittest.main()
