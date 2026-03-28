"""
Diagnostic server: runs Django WSGI import (with a 30s timeout), stores
any error, starts HTTP server, then returns result from /ping/.
Visit /ping/ in browser after deploy to see the Django import result.
"""
import os
import sys
import json
import signal
import traceback
import http.server

PORT = int(os.environ.get("PORT", 8000))

# ── Try importing Django WSGI ──────────────────────────────────────────────
django_ok = False
error_text = None


def _timeout(signum, frame):
    raise TimeoutError("Django WSGI import timed out after 30s")


signal.signal(signal.SIGALRM, _timeout)
signal.alarm(30)
try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oromolegacy.settings")
    from oromolegacy.wsgi import application  # noqa: F401
    signal.alarm(0)
    django_ok = True
except Exception:
    signal.alarm(0)
    error_text = traceback.format_exc()


# ── Serve ──────────────────────────────────────────────────────────────────
class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        payload = {"django_ok": django_ok, "error": error_text,
                   "port": PORT, "python": sys.version}
        body = json.dumps(payload, indent=2).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        pass  # suppress access logs


print(f"Serving on port {PORT}. Visit /ping/ to see Django import result.",
      flush=True)
http.server.HTTPServer(("", PORT), Handler).serve_forever()
