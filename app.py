"""PayPilot — zero-dependency web server (Python stdlib only).

Run:  python3 app.py [port]      ->  http://localhost:8000
Env (all optional):
  OPENAI_API_KEY / OPENAI_BASE_URL / OPENAI_MODEL — AI parsing (else fallback)
  PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET / PAYPAL_MERCHANT_EMAIL — sandbox
"""
import json
import os
import sys
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

import ai_parser
import paypal_client

HERE = os.path.dirname(os.path.abspath(__file__))


class Handler(BaseHTTPRequestHandler):
    server_version = "PayPilot/0.1"

    def _json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _file(self, path, ctype):
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            return self._file(os.path.join(HERE, "static", "index.html"),
                              "text/html; charset=utf-8")
        if self.path == "/api/health":
            return self._json({
                "ok": True,
                "ai": bool(os.environ.get("OPENAI_API_KEY")),
                "paypal": "sandbox" if os.environ.get("PAYPAL_CLIENT_ID")
                         else "mock",
            })
        self.send_error(404)

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length).decode() or "{}")
        except Exception:
            return self._json({"error": "invalid JSON"}, 400)

        if self.path == "/api/parse":
            text = (data.get("description") or "").strip()
            if not text:
                return self._json({"error": "description required"}, 400)
            return self._json(ai_parser.parse(text))

        if self.path == "/api/invoice":
            parsed = data.get("parsed")
            email = (data.get("email") or "").strip()
            if not parsed or not email or "@" not in email:
                return self._json({"error": "parsed invoice + recipient email required"}, 400)
            try:
                return self._json(paypal_client.create_invoice(parsed, email))
            except Exception as e:  # sandbox errors stay visible, never crash
                return self._json({"error": f"PayPal error: {e}"}, 502)

        self.send_error(404)

    def log_message(self, *args):
        pass  # quiet


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    srv = HTTPServer(("127.0.0.1", port), Handler)
    print(f"PayPilot running on http://127.0.0.1:{port} (Ctrl-C to stop)")
    srv.serve_forever()
