# CuteSOC ♡

CuteSOC es un pequeño Security Operations Center de práctica: detección de eventos sospechosos con Python, Flask y SQLite, más un prototipo estático interactivo para GitHub Pages.

## Backend local Flask + SQLite

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m analyzer.log_parser
python app.py
```

Abrí `http://127.0.0.1:5000`.

La aplicación Flask usa `templates/index.html` y `static/`. Esos archivos se mantienen separados de `docs/`, que es la versión estática de GitHub Pages.

## Tests

```powershell
python -m unittest discover -s tests -v
```

## Estructura

```text
app.py                  Backend Flask
analyzer/               Parser y reglas de detección
database/               Acceso SQLite
data/                   Logs de muestra
static/                 CSS y JavaScript del dashboard Flask
templates/index.html    Plantilla Jinja del backend
docs/index.html         Prototipo estático para GitHub Pages
docs/assets/            CSS y JavaScript estáticos
tests/                  Pruebas unitarias
```
