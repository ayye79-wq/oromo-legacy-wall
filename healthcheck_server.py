"""
Minimal diagnostic server - no Django, no gunicorn.
If this passes Railway's healthcheck, the issue is Django/gunicorn startup.
If this also fails, the issue is Railway's port routing.
"""
import os
import sys
import http.server
import json

print("=== DIAGNOSTIC SERVER ===", flush=True)
print(f"Python: {sys.version}", flush=True)
print(f"PORT env: {os.environ.get('PORT', 'NOT SET')}", flush=True)
print(f"All env keys: {[k for k in os.environ.keys()]}", flush=True)

PORT = int(os.environ.get("PORT", 8000))
print(f"Binding to port: {PORT}", flush=True)


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"status": "ok", "port": PORT}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        print(f"[HTTP] {fmt % args}", flush=True)


server = http.server.HTTPServer(("", PORT), Handler)
print(f"Listening on 0.0.0.0:{PORT}", flush=True)
server.serve_forever()
