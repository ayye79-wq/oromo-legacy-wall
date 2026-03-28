"""
Diagnostic: imports Django WSGI in a background thread and logs any errors.
Healthcheck always passes so we can see the full traceback in Deploy Logs.
"""
import os
import sys
import json
import threading
import traceback
import http.server

PORT = int(os.environ.get("PORT", 8000))
print(f"=== DIAG SERVER port={PORT} ===", flush=True)
print(f"Python: {sys.version}", flush=True)


def try_django():
    print("--- Attempting Django WSGI import ---", flush=True)
    try:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oromolegacy.settings")
        from oromolegacy.wsgi import application
        print("=== DJANGO WSGI IMPORT OK ===", flush=True)
    except Exception as e:
        print("=== DJANGO WSGI IMPORT FAILED ===", flush=True)
        traceback.print_exc(file=sys.stdout)
        sys.stdout.flush()


threading.Thread(target=try_django, daemon=True).start()


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b'{"status":"ok"}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[REQ] {fmt % args}", flush=True)


print(f"Serving on 0.0.0.0:{PORT}", flush=True)
http.server.HTTPServer(("", PORT), Handler).serve_forever()
