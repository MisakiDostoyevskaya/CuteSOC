from pathlib import Path

from flask import Flask, render_template, request

from database.db import get_alerts, initialize_db

BASE_DIR = Path(__file__).resolve().parent

# Absolute paths: templates and CSS are found no matter which folder
# the app is launched from.
app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
    static_url_path="/static",
)

# Never let the browser keep an old copy of style.css / dashboard.js.
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True

VALID_SEVERITIES = {"HIGH", "MEDIUM", "LOW"}

# Prepare the database if it does not exist yet.
initialize_db()


def asset_version(filename):
    """Return the file's modification time, used to bust the cache."""
    try:
        return int((BASE_DIR / "static" / filename).stat().st_mtime)
    except OSError:
        return 0


@app.context_processor
def inject_asset_version():
    return {"asset_version": asset_version}


@app.route("/")
def dashboard():
    alerts = get_alerts()

    severity = request.args.get("severity", "").upper()
    if severity not in VALID_SEVERITIES:
        severity = ""
    ip_query = request.args.get("ip", "").strip()

    filtered_alerts = [
        alert for alert in alerts
        if (not severity or alert["severity"] == severity)
        and (not ip_query or ip_query.lower() in alert["source_ip"].lower())
    ]

    stats = {
        "total_alerts": len(alerts),
        "high_alerts": sum(
            1 for alert in alerts if alert["severity"] == "HIGH"
        ),
        "medium_alerts": sum(
            1 for alert in alerts if alert["severity"] == "MEDIUM"
        ),
        "unique_ips": len({
            alert["source_ip"] for alert in alerts
        }),
    }

    return render_template(
        "index.html",
        alerts=filtered_alerts,
        stats=stats,
        severity=severity,
        ip_query=ip_query,
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
