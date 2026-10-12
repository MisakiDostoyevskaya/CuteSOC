
import json
from pathlib import Path

from analyzer.detection_rules import (
    detect_brute_force,
    detect_port_scan,
)
from database.db import initialize_db, save_alert


def load_logs(file_path):
    """Load security events from a JSON file."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    if not isinstance(logs, list):
        raise ValueError("The log file must contain a JSON list.")

    return logs


def main():
    project_root = Path(__file__).resolve().parent.parent
    logs_path = project_root / "data" / "sample_logs.json"

    logs = load_logs(logs_path)

    brute_force_alerts = detect_brute_force(logs)
    port_scan_alerts = detect_port_scan(logs)

    alerts = brute_force_alerts + port_scan_alerts

    initialize_db()

    for alert in alerts:
        save_alert(alert)

    print("=== CuteSOC Security Alerts ===")
    print(f"Events analyzed: {len(logs)}")
    print(f"Brute-force alerts: {len(brute_force_alerts)}")
    print(f"Port-scan alerts: {len(port_scan_alerts)}")
    print(f"Alerts processed: {len(alerts)}")

    for alert in alerts:
        print(f"\n[{alert['severity']}] {alert['event']}")
        print(f"Source IP: {alert['source_ip']}")
        print(f"Count: {alert['failed_attempts']}")
        print(f"Status: {alert['status']}")


if __name__ == "__main__":
    main()
