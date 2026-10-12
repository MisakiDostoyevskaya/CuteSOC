from collections import Counter, defaultdict


def detect_brute_force(logs, threshold=3):
    """Detect repeated failed logins from the same IP."""
    failed_attempts = Counter(
        event.get("source_ip", "unknown")
        for event in logs
        if event.get("event_type") == "login_failed"
    )

    alerts = []

    for ip_address, count in failed_attempts.items():
        if count >= threshold:
            alerts.append({
                "severity": "HIGH",
                "event": "Multiple failed login attempts",
                "source_ip": ip_address,
                "failed_attempts": count,
                "status": "Suspicious activity detected",
            })

    return alerts


def detect_port_scan(logs, threshold=5):
    """Detect possible port scans from connections to distinct ports."""
    ports_by_ip = defaultdict(set)

    for event in logs:
        if event.get("event_type") != "connection_attempt":
            continue

        source_ip = event.get("source_ip")
        port = event.get("destination_port")

        if not source_ip:
            continue

        if not isinstance(port, int) or isinstance(port, bool):
            continue

        if not 1 <= port <= 65535:
            continue

        ports_by_ip[source_ip].add(port)

    alerts = []

    for ip_address, ports in ports_by_ip.items():
        if len(ports) >= threshold:
            alerts.append({
                "severity": "MEDIUM",
                "event": "Possible port scan detected",
                "source_ip": ip_address,
                "failed_attempts": len(ports),
                "status": "Multiple destination ports contacted",
            })

    return alerts
