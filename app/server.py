import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    server_version = "DevSecOpsLab"
    sys_version = ""

    def respond(self, status, content_type, body):
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Content-Security-Policy", "default-src 'none'; frame-ancestors 'none'; base-uri 'none'; form-action 'none'")
        self.send_header("Permissions-Policy", "geolocation=(), microphone=(), camera=()")
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/healthz":
            self.respond(200, "application/json", json.dumps({"status": "ok", "service": "gke05-qas-devsecops-lab"}))
        elif path == "/":
            self.respond(200, "text/html; charset=utf-8", "<!doctype html><html lang='en'><head><meta charset='utf-8'><title>GKE05 QAS DevSecOps Lab</title></head><body><h1>GKE05 QAS DevSecOps Lab</h1><p>Isolated deployment for verified security testing.</p></body></html>")
        else:
            self.respond(404, "application/json", '{"error":"not_found"}')

    def do_POST(self):
        self.respond(405, "application/json", '{"error":"method_not_allowed"}')

port = int(os.getenv("PORT", "8080"))
ThreadingHTTPServer(("0.0.0.0", port), Handler).serve_forever()
