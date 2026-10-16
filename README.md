# CuteSOC ♡

A tiny Security Operations Center dashboard built with Python, Flask and SQLite.
It reads security logs, detects suspicious behaviour and shows the alerts in a cute dark-lilac dashboard.

## Features

- **Brute-force detection**: repeated `login_failed` events from the same IP.
- **Port-scan detection**: one IP contacting many distinct destination ports.
- **Dashboard**: stats cards, severity/IP filters, sortable columns, click an IP to copy it, press `/` to search.

## Project layout

```
app.py                  Flask app (dashboard)
analyzer/               log parser + detection rules
database/               SQLite helpers (cutesoc.db is created automatically)
data/sample_logs.json   sample events
static/                 style.css, dashboard.js
templates/index.html    dashboard template
tests/                  unit tests
```

## Run it

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python -m analyzer.log_parser   # analyze data/sample_logs.json and save alerts
python app.py                   # then open http://127.0.0.1:5000
```

> ⚠️ Open the dashboard through the Flask URL above. Double-clicking
> `templates/index.html` will show an unstyled page, because the template needs
> Flask to resolve `{{ url_for(...) }}` and serve `/static/style.css`.

## Tests

```bash
python -m unittest discover -v
```

## Troubleshooting: "the CSS isn't applied"

1. Make sure you opened `http://127.0.0.1:5000`, not the `.html` file.
2. Hard-refresh the browser (Ctrl+F5 / Cmd+Shift+R). The app already disables static caching and versions the CSS URL.
3. Check that `http://127.0.0.1:5000/static/style.css` loads in the browser.
