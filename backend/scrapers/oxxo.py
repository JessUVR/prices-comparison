import requests
from bs4 import BeautifulSoup

def get_promotions():
    url = "https://www.oxxo.com/promociones/cerveza-vinos-y-licores"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    promos = soup.select("div.promotion_image")

    results = []

    for p in promos:
        try:
            img = p.find("img")
            title = img.get("alt", "").strip()
            image = img.get("src", "").strip()
            onclick = img.get("onclick", "")
            valid_until = "Not available"

            if onclick:
                parts = onclick.split("'")
                if len(parts) >= 10:
                    valid_until = parts[9].strip()

            results.append({
                "name": title,
                "image": image,
                "valid_until": valid_until,
                "store": "OXXO"
            })
        except Exception:
            continue

    return results

def run():
    return get_promotions()
