# backend/scrapers/soriana_promos.py

from typing import List, Dict, Optional
from urllib.parse import urljoin
from decimal import Decimal
from bs4 import BeautifulSoup

from .scraper_utils import (
    fetch_html, text_of, is_price_like,
    normalize_price, normalize_currency,
    extract_product_from_pdp, validate_with_offer,
    now_utc_iso,
)

# ---- Config ----
START_URL = (
    "https://www.soriana.com/vinos-licores-y-cervezas/ofertas/"
    "?showMedia=true&cgid=oferta-vinos-licores-y-cervezas&view=grid&offer=true&showMedia=true"
)
BASE_URL     = "https://www.soriana.com"
ENRICH_LIMIT = 10  # cuántas PDP consultar para completar datos

# ---- Selectores del grid ----
CARD_SEL  = ".product-card, .product-tile, li.product, [data-product-id]"
TITLE_SEL = ".product-tile--link, .product-name, h2 a, a[title], a"
PRICE_SEL = ".price__current, .price-current, .price .current, .price, [data-price], .amount, .product-price"
LINK_SEL  = "a.product-link, .product-tile--link, h2 a, a[href]"

# ---- Parseo del grid (titulo/link/precio crudo) ----
def parse_product_cards(html: str) -> List[Dict[str, str]]:
    soup, out = BeautifulSoup(html, "html.parser"), []
    for card in soup.select(CARD_SEL):
        title_el = card.select_one(TITLE_SEL)
        raw_title = text_of(title_el)
        if title_el is not None and title_el.name == "a":
            raw_href = (title_el.get("href") or "").strip()
        else:
            link_el = card.select_one(LINK_SEL)
            raw_href = (link_el.get("href") or "").strip() if link_el else ""
        price_el = card.select_one(PRICE_SEL)
        raw_price = text_of(price_el)
        if not is_price_like(raw_price):
            raw_price = ""
            for i, desc in enumerate(card.find_all(True)):
                if i > 40: break
                t = text_of(desc)
                if is_price_like(t):
                    raw_price = t; break
        if raw_title or raw_href:
            out.append({"raw_title": raw_title, "raw_price": raw_price, "raw_href": raw_href})
    return out

# ---- Normalización local de items ----
def normalize_item(item: dict, base_url: str, default_currency="MXN") -> Optional[Dict]:
    title = " ".join((item.get("raw_title") or "").split())
    price_amount = normalize_price(item.get("raw_price") or "")
    price_currency = normalize_currency(item.get("raw_price") or "", default_currency)
    url = urljoin(base_url, item.get("raw_href") or "")
    if not url: return None
    if price_amount and Decimal(price_amount) <= 0: price_amount = None
    return {
        "title": title,
        "price_amount": price_amount,
        "price_currency": price_currency,
        "url": url,
        "scraped_at": now_utc_iso(),
    }

def normalize_items(items: list, base_url: str, default_currency="MXN") -> List[Dict]:
    return [x for x in (normalize_item(it, base_url, default_currency) for it in items) if x]

# ---- Main ----
if __name__ == "__main__":
    html = fetch_html(START_URL)
    if not html:
        print("No HTML returned."); raise SystemExit(1)

    raw_items  = parse_product_cards(html)
    norm_items = normalize_items(raw_items, base_url=BASE_URL)

    # Completar título y precio desde PDP (JSON-LD) para las primeras N
    for it in norm_items[:ENRICH_LIMIT]:
        pdp_html = fetch_html(it["url"])
        name, price, curr = extract_product_from_pdp(pdp_html)
        if name and not it.get("title"): it["title"] = name
        if price:
            it["price_amount"]   = normalize_price(price)
            it["price_currency"] = normalize_currency(curr or "", "MXN")

    ready = [x for x in norm_items if x.get("title") and x.get("price_amount")]
    validos, rechazados = validate_with_offer(ready, store_slug="soriana")

    print(f"Válidos: {len(validos)} | Rechazados: {len(rechazados)}")
    for o in validos[:30]:
        print(f"- {o['title']} | ${o['current_price']} {o['currency']} | {o['url']}")
