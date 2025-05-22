import requests
from bs4 import BeautifulSoup

def get_promotions():
    url = "https://www.soriana.com/vinos-licores-y-cervezas/ofertas/?showMedia=true&cgid=oferta-vinos-licores-y-cervezas&view=grid&offer=true&showMedia=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    product_cards = soup.select("div.product")

    promotions = []

    for product in product_cards:
        try:
            name = product.select_one(".product-tile--link").text.strip()
            current_price = product.select_one(".price-pdp").text.strip()
            original_price = product.select_one(".strike-through").text.strip() if product.select_one(".strike-through") else ""
            promotion_badges = product.select(".product-badge")
            promotion_text = ", ".join([badge.get("title", "").strip() for badge in promotion_badges if badge.get("title")])
            image = product.select_one("img").get("src", "").strip()
            requires_coupon = bool(product.select_one(".badge-div-coupons"))

            promotions.append({
                "name": name,
                "current_price": current_price,
                "original_price": original_price,
                "promotion": promotion_text,
                "image": image,
                "requires_coupon": requires_coupon,
                "store": "Soriana"
            })
        except Exception:
            continue

    return promotions

def run():
    return get_promotions()
