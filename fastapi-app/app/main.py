import html
import os
import socket
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

APP_NAME = os.getenv("APP_NAME", "SWE40006 Container Status")
APP_ENV = os.getenv("APP_ENV", "development")
APP_VERSION = os.getenv("APP_VERSION", "0.0.0")
ACCENT_COLOUR = os.getenv("ACCENT_COLOUR", "#2563eb")

app = FastAPI(title=APP_NAME, version=APP_VERSION)


def runtime_info() -> dict:
    return {
        "environment": APP_ENV,
        "version": APP_VERSION,
        "container_hostname": socket.gethostname(),
        "server_time_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }


@app.get("/", response_class=HTMLResponse)
def index():
    rows = "".join(
        f"<tr><th>{html.escape(k.replace('_', ' ').title())}</th>"
        f"<td>{html.escape(str(v))}</td></tr>"
        for k, v in runtime_info().items()
    )
    return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>{html.escape(APP_NAME)}</title>
<style>
body {{ font-family: system-ui, sans-serif; max-width: 640px; margin: 48px auto; padding: 0 16px; }}
h1 {{ color: {html.escape(ACCENT_COLOUR)}; }}
th {{ text-align: left; padding: 6px 24px 6px 0; }}
</style></head>
<body>
<h1>{html.escape(APP_NAME)}</h1>
<p>SWE40006 Task 4.3 - FastAPI in Docker</p>
<table>{rows}</table>
<p>JSON: <a href="/api/info">/api/info</a> &middot; Health: <a href="/health">/health</a></p>
</body></html>"""


@app.get("/api/info")
def api_info():
    return runtime_info()


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}
