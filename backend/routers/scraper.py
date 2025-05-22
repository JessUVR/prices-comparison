from fastapi import APIRouter
from backend.scrapers import oxxo, soriana_prices, soriana_promos

router = APIRouter()

@router.get("/scraper/{store}")
def run_scraper(store: str):
    if store == "soriana":
        products = soriana_prices.run()
    elif store == "soriana_promos":
        products = soriana_promos.run()
    elif store == "oxxo":
        products = oxxo.run()
    else:
        return {"error": "Unsupported store"}

    return {"store": store, "products": products}


@router.get("/scraper/all")
def run_all_scrapers():
    stores = [
        ("soriana", soriana_prices.run),
        ("soriana_promos", soriana_promos.run),
        ("oxxo", oxxo.run),
    ]
    results = {}

    for name, function in stores:
        try:
            results[name] = function()
        except Exception as e:
            results[name] = f"Error: {str(e)}"

    return results
