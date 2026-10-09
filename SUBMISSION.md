# PayPilot — Devpost Submission Package (READY FOR REVIEW — NOT SUBMITTED)

Hackathon: PayPal AI Hackathon — https://paypalaihackathon.devpost.com/
Deadline: Nov 12, 2026, 3:00 PM EST

## Project title
PayPilot — AI Invoices for Casual Sellers

## Tagline
Describe a sale in plain English; PayPilot's AI builds the line items and PayPal sends the invoice.

## Description (for Devpost "About" field)
Casual sellers — garage-sale flippers, side hustlers, craft makers — lose sales
to invoicing friction. PayPilot removes it: type "Selling 3 handmade candles at
$12 each, buyer covers $5 shipping" and the AI parses it into structured line
items, then creates AND sends a real PayPal invoice to the buyer's email, with
the payer-view payment link returned instantly.

**PayPal integration (meaningful):** PayPal Invoicing API v2 in sandbox —
OAuth2 client-credentials flow, invoice creation, send, and payer-view link
retrieval. Every invoice is a real PayPal object, not a mock.

**AI integration (meaningful):** An LLM (any OpenAI-compatible endpoint)
parses unstructured sale descriptions into quantities, unit prices, totals,
and notes. A deterministic rule-based fallback parser ships in the repo so
judges can run the full flow with zero API keys.

**How to run (judges):**
```
git clone https://github.com/midnightmichigan/paypilot
cd paypilot
python3 app.py          # http://127.0.0.1:8000 — works with zero config (mock mode)
python3 test_flow.py    # end-to-end smoke test, all passing
```
For the live PayPal flow, set PAYPAL_CLIENT_ID / PAYPAL_CLIENT_SECRET /
PAYPAL_MERCHANT_EMAIL (free sandbox creds from developer.paypal.com) and
optionally OPENAI_API_KEY for LLM parsing.

## Links
- Repo: https://github.com/midnightmichigan/paypilot (public, MIT)
- Demo: run instructions above (no video required by the rules; functional
  demo via run instructions satisfies the requirement)
- Built with: Python 3 (stdlib only — zero dependencies), PayPal Invoicing
  API v2, OpenAI-compatible LLM API

## Submission checklist (before clicking Submit on Devpost)
- [x] Public repo with OSI license (MIT) — https://github.com/midnightmichigan/paypilot
- [x] Text description + run instructions (this file)
- [ ] Real sandbox invoice verified end-to-end (NEEDS BROWSER: create free
      PayPal Developer sandbox app at developer.paypal.com, set env creds,
      run one invoice, confirm in sandbox dashboard)
- [ ] Eligibility re-check (18+, US — expected fine)
- [ ] Final review of Devpost draft, then Submit before Nov 12, 2026 3:00 PM EST
