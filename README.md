# PayPilot — AI invoice generator for casual sellers

Entry for the **PayPal AI Hackathon** ($67,500 prizes, deadline Nov 12, 2026).

## What it does
Casual sellers (garage sales, side hustles, marketplace flippers) describe a sale
in plain English. PayPilot's AI turns the description into invoice line items,
then creates and sends a real **PayPal sandbox invoice** to the buyer's email —
no accounting knowledge, no manual line-item entry.

Example: *"Selling 3 handmade candles at $12 each, buyer covers $5 shipping"*
→ 3 × Handmade candles @ $12.00 = $36.00 → PayPal invoice emailed to the buyer.

## Why it fits the hackathon
- **Meaningfully integrates PayPal**: PayPal Invoicing API v2 (sandbox) —
  creates the invoice AND sends it, returns the payer-view payment link.
- **Meaningfully incorporates AI**: LLM parses unstructured sale descriptions
  into structured invoice items (quantities, unit prices, totals).
- **Working prototype**: zero-dependency Python server; judges can run
  `python3 app.py` with no API keys (deterministic fallback parser + mock
  PayPal mode), or plug in sandbox creds for the live flow.

## Run it
```
python3 app.py            # http://127.0.0.1:8000
python3 test_flow.py      # end-to-end smoke test (parse + mock invoice)
```

## Optional env (real modes)
- `OPENAI_API_KEY` (+ `OPENAI_BASE_URL`, `OPENAI_MODEL`) — AI parsing.
  Any OpenAI-compatible endpoint works. Without it, the built-in rule-based
  parser handles common phrasings.
- `PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_MERCHANT_EMAIL` —
  free sandbox credentials from https://developer.paypal.com. Without them,
  invoice creation runs in mock mode (clearly labeled in the UI).

## Submission status
**DRAFT — NOT SUBMITTED.** Ready-for-review items before submission:
1. Create the free PayPal Developer sandbox app, run one real sandbox
   invoice end-to-end, screenshot the payer-view link.
2. Record a demo walkthrough (rules require a functional demo, no video
   required — setup instructions or hosted URL satisfy it).
3. Push to a public GitHub repo under midnightmichigan with an OSI license.
4. Confirm official-rules eligibility (18+, US resident — expected fine).
5. Polish item-name cleanup in the fallback parser — DONE 2026-10-15
   (shipping clauses, unit markers, filler words stripped; all tests pass).
6. DEMO.md scripted walkthrough written — DONE 2026-10-15 (no video
   required by rules; functional demo via app + walkthrough).

## Files
- `app.py` — stdlib HTTP server, routes `/`, `/api/health`, `/api/parse`, `/api/invoice`
- `ai_parser.py` — LLM parser (OpenAI-compatible) + deterministic fallback
- `paypal_client.py` — PayPal Invoicing API v2 wrapper + labeled mock mode
- `static/index.html` — single-page UI
- `test_flow.py` — end-to-end smoke test (all passing)
- `HUNT-LOG.md` — how this opportunity was found and what was skipped
