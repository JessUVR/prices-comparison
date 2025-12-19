from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict, List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .scraped_offer import ScrapedOffer


# CONFIG

BASE_URL = "https://adomicilio.merco.mx"
CATEGORY_URL = (
    "https://adomicilio.merco.mx/c/cervezas-vinos-y-licores-vkx8dnq7x5"
)


# HTML + NEXT HELPERS

def fetch_html(url: str) -> str:
    resp = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123 Safari/537.36"
            )
        },
        timeout=20,
    )
    resp.raise_for_status()
    return resp.text


def extract_next_data(html: str) -> Dict[str, Any]:
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find("script", id="__NEXT_DATA__")
    if not script or not script.string:
        raise RuntimeError("__NEXT_DATA__ <script> not found in page")
    return json.loads(script.string)


def get_apollo_state(data: Dict[str, Any]) -> Dict[str, Any]:
    """Search for apolloState in props."""
    props = data.get("props", {})

    apollo = props.get("apolloState")
    if apollo:
        return apollo

    # rare fallback
    apollo = props.get("pageProps", {}).get("apolloState")
    if apollo:
        return apollo

    raise RuntimeError("apolloState not found in __NEXT_DATA__")


def find_catalog_search_key(apollo: Dict[str, Any]) -> str:
    root = apollo.get("ROOT_QUERY", {})

    for key in root.keys():
        if key.startswith("catalogSearch(") and "category:Cervezas, Vinos y Licores" in key:
            print(f"[MERCO] Using catalogSearch key: {key}")
            return key

    # fallback
    for key in root.keys():
        if key.startswith("catalogSearch("):
            print(f"[MERCO] Using FIRST catalogSearch key: {key}")
            return key

    raise RuntimeError("No catalogSearch() key found in apolloState")


# PRODUCT -> ScrapedOffer

def product_to_scraped_offer(prod: Dict[str, Any]) -> ScrapedOffer:
    """Extrae name, photo, price, url."""
    # --- title ---
    title = prod.get("name", "").strip()

    # --- image ---
    photo = prod.get("defaultPhoto")
    image_url = None

    if isinstance(photo, str):
        # Current Merco case: comes as URL string
        image_url = photo
    elif isinstance(photo, dict):
        # In case it changes to an object in the future
        image_url = (
            photo.get("url")
            or photo.get("thumbnailUrl")
            or photo.get("secureUrl")
            or photo.get("secure_url")
        )

    # --- price ---
    pricing = prod.get("pricing", {})
    price_str = pricing.get("price")
    try:
        price = float(price_str)
    except Exception:
        price = None

    # --- slug / Product URL ---
    slug = prod.get("slug")
    product_url = urljoin(BASE_URL, f"/p/{slug}") if slug else None

    return ScrapedOffer(
        store_code="merco",
        title=title,
        price=price,
        validity_text=None,
        image_url=image_url,
        product_url=product_url,
    )


# MAIN SCRAPER

def scrape_offers() -> List[ScrapedOffer]:
    print("[MERCO] Fetching category page...")
    html = fetch_html(CATEGORY_URL)

    print("[MERCO] Extracting __NEXT_DATA__...")
    data = extract_next_data(html)

    print("[MERCO] Extracting apolloState...")
    apollo = get_apollo_state(data)

    key = find_catalog_search_key(apollo)
    section = apollo["ROOT_QUERY"][key]

    items = section.get("items", [])
    print(f"[MERCO NEXT_DATA] items in catalogSearch = {len(items)}")

    offers: List[ScrapedOffer] = []

    for ref in items:
        ref_id = ref["__ref"]  # ejemplo: "Product:UHJvZHVjdDo1MDYzNjQ="
        prod = apollo.get(ref_id, {})

        print("\n[MERCO DEBUG] RAW PRODUCT OBJECT")
        print(f"ref = {ref_id}")
        print("keys:", list(prod.keys()))

        try:
            offer = product_to_scraped_offer(prod)
            offers.append(offer)
        except Exception as e:
            print("[MERCO ERROR] Could not convert product:", e)

    print(f"\n[MERCO] Total Merco offers scraped: {len(offers)}")
    return offers


# MAIN GUARD

if __name__ == "__main__":
    import traceback

    print("[MERCO] __main__ started")

    try:
        scraped = scrape_offers()

        print("\n[MERCO] FINAL RESULT ======")
        for o in scraped:
            print("-", o.title, o.price, o.image_url, o.product_url)

    except Exception as e:
        print("\n[MERCO ERROR] Exception in scrape_offers():")
        traceback.print_exc()