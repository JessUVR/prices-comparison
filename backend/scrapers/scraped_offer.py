from dataclasses import dataclass
from typing import Optional


@dataclass
class ScrapedOffer:
    store_code: str                 # "oxxo", "soriana", "seven", etc.
    title: str                      # offer title or product name
    price: Optional[float]          # may be None if the store doesn't provide a price
    validity_text: Optional[str]    # text like "Valid from X to Y"
    image_url: Optional[str]        # URL to the promo or product image
    product_url: Optional[str] = None  # link to the promo page, if available
