import socket
from datetime import datetime, timezone

from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return (
        "<h1>SWE40006 Task 4.2 - Flask in Docker</h1>"
        f"<p>Container hostname: {socket.gethostname()}</p>"
        f"<p>Server time (UTC): {datetime.now(timezone.utc):%Y-%m-%d %H:%M:%S}</p>"
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
