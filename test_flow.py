"""End-to-end smoke test: boots the server, hits /api/health, /api/parse,
/api/invoice (mock mode), and asserts a sane invoice comes back."""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:18099"


def post(path, payload):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode())


def get(path):
    with urllib.request.urlopen(BASE + path, timeout=15) as r:
        return json.loads(r.read().decode())


proc = subprocess.Popen([sys.executable, "app.py", "18099"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    for _ in range(50):
        try:
            health = get("/api/health")
            break
        except Exception:
            time.sleep(0.2)
    else:
        raise RuntimeError("server did not start")

    assert health["ok"] is True, health
    assert health["paypal"] == "mock", health  # no creds in test env

    parsed = post("/api/parse", {"description": "Selling 3 handmade candles at $12 each"})
    assert parsed["items"], parsed
    assert abs(parsed["total"] - 36.0) < 0.01, parsed
    print("parse OK:", parsed["items"], "total", parsed["total"])

    inv = post("/api/invoice", {"parsed": parsed, "email": "buyer@example.com"})
    assert inv["id"].startswith("INV2-MOCK-"), inv
    assert inv["total"] == 36.0, inv
    assert inv["payer_view_url"], inv
    print("invoice OK:", inv["id"], inv["status"])

    bad = post("/api/parse", {"description": ""})
    assert "error" in bad, bad
    print("validation OK")

    print("ALL TESTS PASSED")
finally:
    proc.terminate()
    proc.wait(timeout=10)
