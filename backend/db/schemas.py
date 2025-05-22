from pydantic import BaseModel
from typing import Optional

# -------- Base schema for an offer --------
class OfferBase(BaseModel):
    description: Optional[str] = None
    discount: Optional[float] = None

# -------- Schema for creating an offer --------
class OfferCreate(OfferBase):
    pass

# -------- Schema for returning an offer --------
class Offer(OfferBase):
    id: int

    model_config = {"from_attributes": True}  # Pydantic v2
