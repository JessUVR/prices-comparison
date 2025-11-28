# backend/scrapers/soriana_promos.py

from typing import List, Dict, Optional
from urllib.parse import urljoin
from decimal import Decimal
from bs4 import BeautifulSoup
import requests

from .scraper_utils import (
    fetch_html, text_of, is_price_like,
    normalize_price, normalize_currency,
    extract_product_from_pdp, validate_with_offer,
    now_utc_iso,
)
from .scraped_offer import ScrapedOffer


# ---- Config ----
START_URL = (
    "https://www.soriana.com/vinos-licores-y-cervezas/ofertas/"
    "?showMedia=true&cgid=oferta-vinos-licores-y-cervezas&view=grid&offer=true&showMedia=true"
)
BASE_URL = "https://www.soriana.com"
ENRICH_LIMIT = 10  # How many product detail pages to fetch for enrichment


# ---- CSS selectors used for scraping ----
CARD_SEL  = ".product-card, .product-tile, li.product, [data-product-id]"
TITLE_SEL = ".product-tile--link, .product-name, h2 a, a[title], a"
PRICE_SEL = ".price__current, .price-current, .price .current, .price, [data-price], .amount, .product-price"
LINK_SEL  = "a.product-link, .product-tile--link, h2 a, a[href]"


# ---- Extract product cards (raw_title, raw_price, raw_href) ----
def parse_product_cards(html: str) -> List[Dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    out = []

    for card in soup.select(CARD_SEL):
        # Extract title
        title_el = card.select_one(TITLE_SEL)
        raw_title = text_of(title_el)

        # Extract product link
        if title_el is not None and title_el.name == "a":
            raw_href = (title_el.get("href") or "").strip()
        else:
            link_el = card.select_one(LINK_SEL)
            raw_href = (link_el.get("href") or "").strip() if link_el else ""

        # Extract price
        price_el = card.select_one(PRICE_SEL)
        raw_price = text_of(price_el)

        # Fallback: search for a price inside descendant nodes
        if not is_price_like(raw_price):
            raw_price = ""
            for i, desc in enumerate(card.find_all(True)):
                if i > 40: 
                    break
                t = text_of(desc)
                if is_price_like(t):
                    raw_price = t
                    break

        if raw_title or raw_href:
            out.append({
                "raw_title": raw_title,
                "raw_price": raw_price,
                "raw_href": raw_href,
            })

    return out


# ---- Normalize each scraped item to a structured dict ----
def normalize_item(item: dict, base_url: str, default_currency="MXN") -> Optional[Dict]:
    title = " ".join((item.get("raw_title") or "").split())
    price_amount = normalize_price(item.get("raw_price") or "")
    price_currency = normalize_currency(item.get("raw_price") or "", default_currency)
    url = urljoin(base_url, item.get("raw_href") or "")

    if not url:
        return None

    # Avoid zero or negative prices
    if price_amount and Decimal(price_amount) <= 0:
        price_amount = None

    return {
        "title": title,
        "price_amount": price_amount,
        "price_currency": price_currency,
        "url": url,
        "scraped_at": now_utc_iso(),
    }


def normalize_items(items: list, base_url: str, default_currency="MXN") -> List[Dict]:
    return [
        x for x in 
        (normalize_item(it, base_url, default_currency) for it in items)
        if x
    ]


# ---- Main scraper function (used by the pipeline) ----
import requests  # Make sure file is above

def scrape_offers() -> List[ScrapedOffer]:
    # 1) Download Soriana offers page using a more realistic browser-like request
    try:
        resp = requests.get(
            START_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/124.0.0.0 Safari/537.36"
                ),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "es-MX,es;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "https://www.soriana.com/",
                "DNT": "1",
            },
            timeout=20,
            allow_redirects=True,
        )
    except Exception as e:
        print(f"Soriana: request failed -> {e}")
        return []

    if resp.status_code != 200:
        print(f"Soriana: bad status code -> {resp.status_code}")
        return []

    html = resp.text

    # 1. Parse raw product cards
    raw_items = parse_product_cards(html)

    # 2. Normalize titles, prices, and URLs
    norm_items = normalize_items(raw_items, base_url=BASE_URL)

    # 3. Optional enrichment from product detail pages
    for it in norm_items[:ENRICH_LIMIT]:
        pdp_html = fetch_html(it["url"])
        if not pdp_html:
            continue

        name, price, curr = extract_product_from_pdp(pdp_html)

        if name and not it.get("title"):
            it["title"] = name

        if price:
            it["price_amount"] = normalize_price(price)
            it["price_currency"] = normalize_currency(curr or "", "MXN")

    # 4. Keep only items with title + price
    ready = [
        x for x in norm_items
        if x.get("title") and x.get("price_amount")
    ]

    # 5. Validate using utils (quality checks)
    validos, rechazados = validate_with_offer(ready, store_slug="soriana")
    print(f"[Soriana] Valid: {len(validos)} | Rejected: {len(rechazados)}")

    # 6. Convert to ScrapedOffer objects for the pipeline
    scraped_offers: List[ScrapedOffer] = []
    for o in validos:
        scraped_offers.append(
            ScrapedOffer(
                store_code="soriana",
                title=o["title"],
                price=float(o["current_price"]),
                validity_text=None,
                image_url=None,   # Soriana offers currently don't include image
                product_url=o["url"],
            )
        )

    return scraped_offers


# ---- CLI test ----
if __name__ == "__main__":
    offers = scrape_offers()
    print("Total Soriana offers:", len(offers))
    for o in offers[:10]:
        print("-", o.title, o.price, o.product_url)
