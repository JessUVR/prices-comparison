from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

# Temporary model (normally defined in schemas.py)
class Product(BaseModel):
    name: str
    price: float
    store: Optional[str] = None
    image: Optional[str] = None

# Temporary in-memory database
products = []

@router.post("/", response_model=Product)
def create_product(product: Product):
    products.append(product)
    return product

@router.get("/", response_model=List[Product])
def get_products():
    return products

@router.get("/search", response_model=List[Product])
def search_product(name: str):
    return [p for p in products if name.lower() in p.name.lower()]
