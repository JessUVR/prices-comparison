# scraper_utils.py
import json, re, requests
from typing import Optional, Tuple, List, Dict
from urllib.parse import urljoin
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from bs4 import BeautifulSoup
from pydantic import ValidationError


# --- HTTP ---
DEFAULT_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
}

def fetch_html(url: str, headers: Optional[Dict] = None, timeout: int = 20) -> str:
    """Simple GET with headers/timeout. Returns the HTML or an empty string if it fails."""
    try:
        r = requests.get(url, headers=headers or DEFAULT_HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except requests.RequestException:
        return ""

# --- Text / Heuristics ---
def text_of(el) -> str:
    """Normalized text from a BeautifulSoup node (collapsed whitespace)."""
    return "" if el is None else " ".join(el.get_text(" ", strip=True).split())

def is_price_like(s: str) -> bool:
    """Very light heuristic to detect strings that look like a price."""
    if not s: return False
    t = s.replace(" ", "")
    return ("$" in t or "MXN" in t or "USD" in t or "€" in t) or any(c.isdigit() for c in t)

# --- Normalization ---
def normalize_price(s: str) -> Optional[str]:
    """Converts a string containing numbers into format '1234.56' (string) or None."""
    if not s: return None
    m = re.findall(r"\d[\d.,]*", s)
    if not m: return None
    t = max(m, key=len)
    if "," in t and "." in t:
        dec = "," if t.rfind(",") > t.rfind(".") else "."
    elif "," in t:
        dec = "," if re.search(r",\d{1,2}$", t) else "."
    elif "." in t:
        dec = "." if re.search(r"\.\d{1,2}$", t) else None
    else:
        dec = None
    if dec == ",": t = t.replace(".", "").replace(",", ".")
    elif dec == ".": t = t.replace(",", "")
    else: t = t.replace(",", "").replace(".", "")
    try:
        return f"{Decimal(t).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"
    except Exception:
        return None

def normalize_currency(s: str, default: str = "MXN") -> str:
    """Attempts to deduce currency from the string; falls back to default."""
    u = (s or "").upper()
    if "USD" in u: return "USD"
    if "MXN" in u or "MX$" in u: return "MXN"
    if "EUR" in u or "€"  in u: return "EUR"
    if "$" in u: return default
    return default

# --- JSON-LD (PDP) ---
def extract_product_from_pdp(html: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Extracts (name, price, currency) from JSON-LD @type Product in a PDP.
    Returns (None, None, None) if not found.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads((tag.string or tag.text or ""))
        except Exception:
            continue
        stack = data if isinstance(data, list) else [data]
        while stack:
            node = stack.pop(0)
            if isinstance(node, dict):
                types = node.get("@type")
                types = [types] if isinstance(types, str) else (types or [])
                if any((t or "").lower() == "product" for t in types):
                    name = (node.get("name") or "").strip() or None
                    offers = node.get("offers", {})
                    if isinstance(offers, list):
                        offers = next((o for o in offers if isinstance(o, dict) and (o.get("price") or o.get("lowPrice"))), {})
                    price = curr = None
                    if isinstance(offers, dict):
                        price = offers.get("price") or offers.get("lowPrice")
                        if price: curr = (offers.get("priceCurrency") or "MXN").upper()
                    if name or price:
                        return name, (str(price) if price else None), curr
                for v in node.values():
                    if isinstance(v, (list, dict)):
                        stack.append(v)
            elif isinstance(node, list):
                stack.extend(node)
    return None, None, None

# --- Misc ---
def now_utc_iso() -> str:
    """ISO8601 timestamp in UTC with Z suffix (no microseconds)."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

from typing import List, Dict, Tuple

def validate_with_offer(items: List[Dict], store_slug: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Very lightweight validation step for scraped items.
    - Keeps items that have a valid title and numeric price_amount.
    - Normalizes the structure to a common dict format.
    - Returns (valid_items, rejected_items).

    NOTE: Preserves extra fields like image_url, scraped_at, product_url if present.
    """
    valid: List[Dict] = []
    rejected: List[Dict] = []

    for it in items:
        title = (it.get("title") or "").strip()
        price_amount = it.get("price_amount")
        price_currency = (it.get("price_currency") or "MXN").strip()
        url = it.get("url")

        # Basic sanity checks
        if not title or price_amount is None or not url:
            rejected.append({"item": it, "reason": "missing title/price/url"})
            continue

        try:
            current_price = float(price_amount)
        except (TypeError, ValueError):
            rejected.append({"item": it, "reason": "invalid numeric price"})
            continue

        # Base payload normalized
        payload: Dict = {
            "title": title,
            "current_price": current_price,
            "currency": price_currency or "MXN",
            "url": url,
            "store_slug": store_slug,
        }

        # 👇 PRESERVE EXTRA FIELDS IF THEY EXIST
        if "image_url" in it:
            payload["image_url"] = it.get("image_url")

        if "scraped_at" in it:
            payload["scraped_at"] = it.get("scraped_at")

        if "product_url" in it:
            payload["product_url"] = it.get("product_url")

        valid.append(payload)

    return valid, rejected

