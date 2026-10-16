
import json
from pathlib import Path

from analyzer.detection_rules import (
    detect_brute_force,
    detect_port_scan,
)
from database.db import initialize_db, save_alert


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOGS_PATH = PROJECT_ROOT / "data" / "sample_logs.json"


def load_logs(file_path=DEFAULT_LOGS_PATH):
    """Load security events from a JSON file."""
    path = Path(file_path)

    with path.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    if not isinstance(logs, list):
        raise ValueError("The log file must contain a JSON list.")

    return logs


def analyze_logs(file_path=DEFAULT_LOGS_PATH):
    """Analyze logs, save detected alerts, and return a summary."""
    logs = load_logs(file_path)

    brute_force_alerts = detect_brute_force(logs)
    port_scan_alerts = detect_port_scan(logs)

    alerts = brute_force_alerts + port_scan_alerts

    initialize_db()

    for alert in alerts:
        save_alert(alert)

    return {
        "events_analyzed": len(logs),
        "brute_force_alerts": len(brute_force_alerts),
        "port_scan_alerts": len(port_scan_alerts),
        "alerts_processed": len(alerts),
    }


def main():
    summary = analyze_logs()

    print("=== CuteSOC Security Alerts ===")
    print(f"Events analyzed: {summary['events_analyzed']}")
    print(f"Brute-force alerts: {summary['brute_force_alerts']}")
    print(f"Port-scan alerts: {summary['port_scan_alerts']}")
    print(f"Alerts processed: {summary['alerts_processed']}")


if __name__ == "__main__":
    main()
