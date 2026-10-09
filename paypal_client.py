"""PayPal Invoicing API (v2) client with sandbox credentials and a mock fallback.

Real mode: set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET (sandbox creds from
https://developer.paypal.com — free). All calls hit the sandbox, never live.
Mock mode: when creds are absent, returns a realistic fake invoice so the app
and judges can run the full flow with zero configuration.
"""
import base64
import json
import os
import time
import urllib.request

SANDBOX = "https://api-m.sandbox.paypal.com"


def _token():
    cid = os.environ["PAYPAL_CLIENT_ID"]
    secret = os.environ["PAYPAL_CLIENT_SECRET"]
    basic = base64.b64encode(f"{cid}:{secret}".encode()).decode()
    req = urllib.request.Request(
        SANDBOX + "/v1/oauth2/token",
        data=b"grant_type=client_credentials",
        headers={"Authorization": "Basic " + basic,
                 "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())["access_token"]


def _api(method, path, token, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        SANDBOX + path, data=data, method=method,
        headers={"Authorization": "Bearer " + token,
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode()
        return json.loads(body) if body else {}


def create_invoice(parsed, recipient_email):
    """Create a draft PayPal invoice. Returns dict with id + links."""
    if not (os.environ.get("PAYPAL_CLIENT_ID")
            and os.environ.get("PAYPAL_CLIENT_SECRET")):
        return _mock_invoice(parsed, recipient_email)
    token = _token()
    items = [{
        "name": i["name"][:127],
        "quantity": str(i.get("quantity", 1)),
        "unit_amount": {"currency_code": parsed.get("currency", "USD"),
                        "value": f"{i.get('unit_price', 0):.2f}"},
    } for i in parsed["items"]]
    payload = {
        "detail": {
            "currency_code": parsed.get("currency", "USD"),
            "note": (parsed.get("notes", "") + " Created with PayPilot.").strip()[:500],
        },
        "invoicer": {"email_address": os.environ.get("PAYPAL_MERCHANT_EMAIL",
                                                     "merchant@example.com")},
        "primary_recipients": [{"billing_info": {"email_address": recipient_email}}],
        "items": items,
    }
    inv = _api("POST", "/v2/invoicing/invoices", token, payload)
    inv_id = inv["id"]
    _api("POST", f"/v2/invoicing/invoices/{inv_id}/send", token, {})
    detail = _api("GET", f"/v2/invoicing/invoices/{inv_id}", token)
    links = {l["rel"]: l["href"] for l in detail.get("links", [])}
    return {"mode": "sandbox", "id": inv_id,
            "status": detail.get("status", "SENT"),
            "payer_view_url": links.get("payer_view", ""),
            "total": parsed.get("total", 0)}


def _mock_invoice(parsed, recipient_email):
    fake_id = f"INV2-MOCK-{int(time.time())}"
    return {
        "mode": "mock",
        "id": fake_id,
        "status": "SENT (mock — set PAYPAL_CLIENT_ID/SECRET for sandbox)",
        "payer_view_url": f"https://www.sandbox.paypal.com/invoice/payerView/details/{fake_id}",
        "recipient": recipient_email,
        "total": parsed.get("total", 0),
    }
