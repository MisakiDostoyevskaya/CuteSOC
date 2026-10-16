
import json

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
)

from analyzer.log_parser import analyze_logs
from database.db import get_alerts, initialize_db

app = Flask(__name__)

# Prepare the database if it does not exist yet.
initialize_db()


@app.route("/")
def dashboard():
    alerts = get_alerts()

    severity = request.args.get("severity", "").upper()
    ip_query = request.args.get("ip", "").strip()

    filtered_alerts = [
        alert for alert in alerts
        if (not severity or alert["severity"] == severity)
        and (
            not ip_query
            or ip_query.lower() in alert["source_ip"].lower()
        )
    ]

    stats = {
        "total_alerts": len(alerts),
        "high_alerts": sum(
            1 for alert in alerts if alert["severity"] == "HIGH"
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
        message=request.args.get("message", ""),
        error=request.args.get("error", ""),
    )


@app.route("/analyze", methods=["POST"])
def run_analysis():
    try:
        summary = analyze_logs()

        message = (
            f"Analysis completed: {summary['events_analyzed']} events "
            f"analyzed and {summary['alerts_processed']} alerts processed."
        )

        return redirect(url_for("dashboard", message=message))

    except (OSError, ValueError, json.JSONDecodeError):
        app.logger.exception("Error analyzing security logs")

        return redirect(
            url_for(
                "dashboard",
                error="Unable to analyze the log file. Check the server logs.",
            )
        )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
