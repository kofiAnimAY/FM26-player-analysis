from app import create_app
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
import os


def run_static_frontend():
    frontend_dir = Path(__file__).resolve().parent / "frontend"
    handler = partial(SimpleHTTPRequestHandler, directory=str(frontend_dir))
    server = ThreadingHTTPServer(("0.0.0.0", 8080), handler)
    server.serve_forever()


if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Thread(target=run_static_frontend, daemon=True).start()

    app = create_app()
    app.run(host="0.0.0.0", port=8000, debug=True)
