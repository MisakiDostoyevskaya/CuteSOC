import unittest

from analyzer.detection_rules import detect_port_scan


class TestPortScanDetection(unittest.TestCase):

    def test_detects_multiple_distinct_ports(self):
        logs = [
            {
                "event_type": "connection_attempt",
                "source_ip": "192.0.2.50",
                "destination_port": port,
            }
            for port in [22, 80, 443, 8080, 3306]
        ]

        alerts = detect_port_scan(logs)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["source_ip"], "192.0.2.50")
        self.assertEqual(alerts[0]["severity"], "MEDIUM")
        self.assertEqual(alerts[0]["failed_attempts"], 5)

    def test_repeated_connections_to_same_port_do_not_trigger(self):
        logs = [
            {
                "event_type": "connection_attempt",
                "source_ip": "192.0.2.50",
                "destination_port": 22,
            }
            for _ in range(10)
        ]

        self.assertEqual(detect_port_scan(logs), [])

    def test_below_threshold_does_not_trigger(self):
        logs = [
            {
                "event_type": "connection_attempt",
                "source_ip": "192.0.2.50",
                "destination_port": port,
            }
            for port in [22, 80, 443, 8080]
        ]

        self.assertEqual(detect_port_scan(logs), [])

    def test_ignores_invalid_ports(self):
        logs = [
            {
                "event_type": "connection_attempt",
                "source_ip": "192.0.2.50",
                "destination_port": 70000,
            },
            {
                "event_type": "connection_attempt",
                "source_ip": "192.0.2.50",
                "destination_port": "443",
            },
        ]

        self.assertEqual(detect_port_scan(logs), [])

    def test_ignores_login_events(self):
        logs = [
            {
                "event_type": "login_failed",
                "source_ip": "192.0.2.50",
                "destination_port": port,
            }
            for port in [22, 80, 443, 8080, 3306]
        ]

        self.assertEqual(detect_port_scan(logs), [])


if __name__ == "__main__":
    unittest.main()