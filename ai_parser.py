"""PayPilot AI parser: turns plain-English sale descriptions into invoice line items.

Uses an LLM when OPENAI_API_KEY is set; otherwise falls back to a
deterministic rule-based parser so the app works with zero configuration.
"""
import json
import os
import re
import urllib.request


def parse_with_llm(text):
    """Ask an OpenAI-compatible chat API to extract invoice items as JSON."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    prompt = (
        "Extract invoice line items from the seller's description. "
        'Return ONLY valid JSON: {"items": [{"name": str, "quantity": number, '
        '"unit_price": number}], "currency": "USD", "notes": str}. '
        "Prices in USD. If no price is stated, use 0 and note it."
    )
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }).encode()
    req = urllib.request.Request(
        base + "/chat/completions", data=body,
        headers={"Authorization": "Bearer " + api_key,
                 "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
        return json.loads(data["choices"][0]["message"]["content"])
    except Exception:
        return None


MONEY = re.compile(r"\$\s?(\d+(?:\.\d{1,2})?)")
QTY = re.compile(r"(\d+)\s*(?:x|pieces?|items?|units?)\b", re.IGNORECASE)
# filler words that pollute the item name in fallback mode
LEAD_VERB = re.compile(r"^\s*(?:selling|sold|sell|for sale)\b", re.IGNORECASE)
UNIT_WORDS = re.compile(
    r"\b(each|apiece|per item|per unit|a piece)\b", re.IGNORECASE)
SHIPPING_CLAUSE = re.compile(
    r"[,;]?\s*(?:and\s+)?(?:buyer|customer)\s+covers?\s+"
    r"\$?\d+(?:\.\d{1,2})?\s*(?:for\s+)?(?:shipping|postage|delivery)\b"
    r"|[,;]?\s*plus\s+\$?\d+(?:\.\d{1,2})?\s*(?:for\s+)?(?:shipping|postage|delivery)\b"
    r"|\+\s*\$?\d+(?:\.\d{1,2})?\s*(?:shipping|postage|delivery)\b",
    re.IGNORECASE)


def clean_item_name(text):
    """Turn a raw description into a presentable invoice item name."""
    # shipping clause first: it matches on the $ amounts MONEY would strip
    name = SHIPPING_CLAUSE.sub("", text)
    name = MONEY.sub("", name)
    name = QTY.sub("", name)
    name = UNIT_WORDS.sub("", name)
    name = LEAD_VERB.sub("", name)
    # bare leading quantity ("3 handmade candles") and trailing prepositions
    name = re.sub(r"^\s*\d+\s+", "", name)
    name = re.sub(r"\s+", " ", name).strip(" ,.-")
    name = re.sub(r"\s+(?:at|for|with|of|in|on)$", "", name, flags=re.IGNORECASE)
    name = (name[:60] + "...") if len(name) > 63 else name
    return name or "Item"


def parse_rule_based(text):
    """Deterministic fallback parser: finds $ amounts and quantities."""
    amounts = [float(m) for m in MONEY.findall(text)]
    # strip prices first so "$12" can't be misread as a quantity
    no_money = MONEY.sub(" ", text)
    qty_m = (QTY.search(no_money)
             or re.search(r"\b(\d+)\s+[a-zA-Z]", no_money))  # bare number + word
    qty = int(qty_m.group(1)) if qty_m else 1
    # cleaned item name: strip prices/quantities/shipping clauses/filler
    name = clean_item_name(text)
    per_unit = bool(re.search(r"\b(each|apiece|per item|per unit|a piece)\b",
                             text, re.IGNORECASE))
    if amounts:
        unit_price = round(amounts[0], 2) if per_unit else round(amounts[0] / qty, 2)
    else:
        unit_price = 0.0
    return {
        "items": [{"name": name, "quantity": qty, "unit_price": unit_price}],
        "currency": "USD",
        "notes": "Parsed with built-in fallback parser (no AI key configured).",
        "total": round(unit_price * qty, 2),
    }


def parse(text):
    result = parse_with_llm(text)
    if result and isinstance(result.get("items"), list):
        items = result["items"]
        total = round(sum(i.get("quantity", 1) * i.get("unit_price", 0)
                          for i in items), 2)
        result.setdefault("currency", "USD")
        result["total"] = total
        result["notes"] = result.get("notes", "") + " [AI-parsed]"
        return result
    return parse_rule_based(text)
