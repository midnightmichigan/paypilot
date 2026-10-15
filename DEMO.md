# PayPilot — Demo Walkthrough

No video required by the official rules; this scripted walkthrough plus the
live app satisfies the functional-demo requirement. Judges: run
`python3 app.py` (zero dependencies, zero config) and open
http://127.0.0.1:8000.

## Scenario: garage-sale seller, no accounting knowledge

**Seller types (plain English):**
> Selling 3 handmade candles at $12 each, buyer covers $5 shipping

**PayPilot shows:**
- Line item: `handmade candles` — 3 × $12.00 = $36.00
- Buyer email field → PayPal sandbox invoice created AND sent
- Payer-view payment link returned instantly

**Two more one-liners to try:**
- `2x vintage lamps $40 apiece plus $8 shipping` → `vintage lamps` 2 × $40.00
- `4 jars of honey for $8 a piece` → `jars of honey` 4 × $8.00

## What the judges are seeing

1. **AI parsing** — with `OPENAI_API_KEY` set, an LLM extracts structured
   items (name, quantity, unit price) from free text. Without a key, the
   built-in deterministic fallback parser handles common phrasings
   (see `ai_parser.py` — shipping clauses, per-unit markers, and filler
   words are stripped so invoice names read clean).
2. **PayPal integration** — `paypal_client.py` wraps PayPal Invoicing API v2:
   OAuth2 client-credentials → create draft invoice → send → payer-view link.
   With `PAYPAL_CLIENT_ID`/`PAYPAL_CLIENT_SECRET`/`PAYPAL_MERCHANT_EMAIL`
   from a free developer.paypal.com sandbox app, the flow is fully live.
   Without them, mock mode runs end-to-end (clearly labeled in the UI) so
   the demo never blocks.
3. **Verification** — `python3 test_flow.py` runs the full parse →
   invoice pipeline and asserts totals (all passing).

## Real-sandbox checklist (pre-submission)

1. Create free app at https://developer.paypal.com → sandbox credentials.
2. `PAYPAL_CLIENT_ID=... PAYPAL_CLIENT_SECRET=... PAYPAL_MERCHANT_EMAIL=... python3 app.py`
3. Submit one invoice to a test buyer email; capture the payer-view link.
