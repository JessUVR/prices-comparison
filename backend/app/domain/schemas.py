from pydantic import BaseModel, Field
from typing import Optional

# 🔹 1. Base schema – defines the common structure shared by all variants
class OfferBase(BaseModel):
    store_id: int = Field(..., description="ID of the store (FK)")
    title: str = Field(..., description="Offer title or product name")
    price: Optional[float] = Field(None, description="Offer price (if available)")
    validity_text: Optional[str] = Field(None, description="Promo description")
    image_url: Optional[str] = Field(None, description="Image URL")

# 🔹 2. Create schema – used for data validation when creating a new record
class OfferCreate(OfferBase):
    pass  # inherits all fields from OfferBase

# 🔹 3. Update schema – used for partial updates (fields are optional)
class OfferUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[float] = None
    validity_text: Optional[str] = None
    image_url: Optional[str] = None

# 🔹 4. Read schema – defines what the API returns to the client
class OfferRead(OfferBase):
    id: int

    class Config:
        from_attributes = True  # allows automatic conversion from SQLAlchemy models
