import re
import requests
from bs4 import BeautifulSoup
from datetime import date
from typing import List
from .scraped_offer import ScrapedOffer


START_URL = "https://www.oxxo.com/promociones/cerveza-vinos-y-licores"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
}

# Basic mapping for Spanish month names
MONTHS_ES = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}


def _first_image_url(img):
    """Get the image URL from the most common attributes (src, data-src, srcset)."""
    # 1) direct src
    u = (img.get("src") or "").strip()
    if u:
        return _abs_url(u)
    # 2) data-src
    u = (img.get("data-src") or "").strip()
    if u:
        return _abs_url(u)
    # 3) srcset: take the first URL before the space
    srcset = (img.get("srcset") or img.get("data-srcset") or "").strip()
    if srcset:
        first = srcset.split(",")[0].strip().split(" ")[0]
        return _abs_url(first)
    return ""


def _abs_url(u):
    """Normalize relative or // URLs to a full https absolute URL."""
    if not u:
        return ""
    if u.startswith("//"):
        return "https:" + u
    if u.startswith("/"):
        return "https://www.oxxo.com" + u
    return u


def _pad2(n):
    """Return day padded to 2 digits (01..31)."""
    return str(n).zfill(2)


def parse_vigencia(texto):
    """
    Try to parse strings like:
      'Vigencia del 1 al 15 de septiembre de 2025'
      'Vigencia del 17 de julio al 20 de agosto de 2025'
    If it cannot parse, returns (None, None, cleaned_text).
    """
    if not texto:
        return None, None, ""

    t = texto.lower().strip()

    # pattern 1: del 17 de julio al 20 de agosto de 2025 ...
    m = re.search(
        r"del\s+(\d{1,2})\s+de\s+([a-záéíóú]+)\s+al\s+(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})(.*)",
        t,
    )
    if m:
        d1, mon1, d2, mon2, year, rest = m.groups()
        m1 = MONTHS_ES.get(mon1.strip(), "")
        m2 = MONTHS_ES.get(mon2.strip(), "")
        vfrom = f"{year}-{m1}-{_pad2(d1)}" if m1 else None
        vuntil = f"{year}-{m2}-{_pad2(d2)}" if m2 else None
        notes = rest.strip(" .")
        return vfrom, vuntil, notes

    # pattern 2 (same month): del 1 al 15 de septiembre de 2025 ...
    m = re.search(
        r"del\s+(\d{1,2})\s+al\s+(\d{1,2})\s+de\s+([a-záéíóú]+)\s+de\s+(\d{4})(.*)",
        t,
    )
    if m:
        d1, d2, mon, year, rest = m.groups()
        mm = MONTHS_ES.get(mon.strip(), "")
        vfrom = f"{year}-{mm}-{_pad2(d1)}" if mm else None
        vuntil = f"{year}-{mm}-{_pad2(d2)}" if mm else None
        notes = rest.strip(" .")
        return vfrom, vuntil, notes

    # if nothing matches, keep the original text as notes
    return None, None, t


def get_promotions():
    """
    Return a list of raw promotions with:
    name, image, valid_from, valid_until, notes, store.
    """
    try:
        r = requests.get(START_URL, headers=HEADERS, timeout=15)
    except Exception:
        return []
    if r.status_code != 200:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    boxes = soup.select("div.promotion_image")
    out = []

    for box in boxes:
        img = box.find("img")
        if not img:
            continue

        name = (img.get("alt") or "").strip()
        image = _first_image_url(img)

        onclick = img.get("onclick", "")
        vig_text = ""
        if onclick:
            parts = onclick.split("'")
            if len(parts) >= 10:
                vig_text = parts[9].strip()

        vfrom, vuntil, notes = parse_vigencia(vig_text)

        out.append(
            {
                "name": name,
                "image": image,
                "valid_from": vfrom,
                "valid_until": vuntil,
                "notes": notes,
                "store": "OXXO",
            }
        )
    return out


def is_active(p, today_iso):
    """
    Return True if today is between [valid_from, valid_until].
    If dates are missing, consider the promo as active.
    """
    vf = p.get("valid_from")
    vu = p.get("valid_until")
    return (not vf or vf <= today_iso) and (not vu or today_iso <= vu)


def scrape_offers() -> List[ScrapedOffer]:
    today = date.today().isoformat()

    raw_items = get_promotions()

    active_items = []
    for promo in raw_items:
        if is_active(promo, today):
            active_items.append(promo)

    scraped_offers: List[ScrapedOffer] = []

    for promo in active_items:
        offer = ScrapedOffer(
            store_code="oxxo",
            title=promo["name"],
            price=None,
            validity_text=promo.get("notes"),
            image_url=promo.get("image"),
            product_url=None,
        )
        scraped_offers.append(offer)

    return scraped_offers



if __name__ == "__main__":
    offers = scrape_offers()

    print("Total active offers:", len(offers))
    print("\nExamples (max 5):")
    for o in offers[:5]:
        print("-")
        print("  store_code :", o.store_code)
        print("  title      :", o.title)
        print("  price      :", o.price)
        print("  validity   :", o.validity_text)
        print("  image      :", o.image_url)
        print("  product    :", o.product_url)