# CuteSOC ♡

CuteSOC es un pequeño Security Operations Center de práctica: detección de eventos sospechosos con Python, Flask y SQLite, más un prototipo estático interactivo para GitHub Pages.

## Demo pública (GitHub Pages)

La versión estática vive en `docs/` y no requiere Python ni un servidor:
- métricas y gráficos ilustrativos
- búsqueda, filtros por severidad y ordenamiento de alertas
- panel de detalle por incidente
- flujo de eventos simulado

**Importante:** la demo de GitHub Pages usa datos ficticios de ejemplo. No está conectada al backend Flask ni monitorea una red real.

Para publicarla:
1. En GitHub, abrí el repositorio `CuteSOC`.
2. Entrá en **Settings → Pages**.
3. En **Build and deployment**, elegí **Deploy from a branch**.
4. Seleccioná la rama `main` y la carpeta `/docs`, y guardá.
5. Esperá a que termine el despliegue. La URL del proyecto debería ser `https://misakidostoyevskaya.github.io/CuteSOC/`.

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
