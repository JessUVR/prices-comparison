from pydantic import BaseModel, Field, HttpUrl, field_validator, model_validator, ConfigDict
from typing import Literal
from datetime import datetime, timezone
from decimal import Decimal
import re

class Offer(BaseModel):
    model_config = ConfigDict(
        extra='forbid',          # reject unknown fields
        validate_assignment=True # re-validate on attribute set
    )

    store_slug: str = Field(..., min_length=2, max_length=32, pattern=r'^[a-z0-9_-]+$')
    title: str
    current_price: Decimal = Field(..., gt=Decimal('0'))
    currency: Literal['MXN', 'USD'] = 'MXN'
    url: HttpUrl
    scraped_at: datetime

    # ---- store_slug: trim, lowercase, slug pattern ----
    @field_validator("store_slug", mode="before")
    @classmethod
    def _strip_lower_slug(cls, v):
        return v.strip().lower() if isinstance(v, str) else v

    # ---- title: trim, not empty ----
    @field_validator("title", mode="before")
    @classmethod
    def _strip_title(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("title")
    @classmethod
    def _title_not_empty(cls, v):
        if not v:
            raise ValueError("title must not be empty")
        return v

    # ---- price: accept "1,234.56", "$99.90", numbers ----
    @field_validator("current_price", mode="before")
    @classmethod
    def _parse_price(cls, v):
        if isinstance(v, str):
            cleaned = re.sub(r"[^\d.\-]", "", v)  # drop currency symbols/commas/spaces
            v = cleaned
        d = Decimal(str(v))
        if d <= 0:
            raise ValueError("current_price must be > 0")
        return d.quantize(Decimal("0.01"))

    # ---- currency: uppercase + restrict via Literal ----
    @field_validator("currency", mode="before")
    @classmethod
    def _upper_currency(cls, v):
        return v.upper() if isinstance(v, str) else v

    # ---- scraped_at: accept ISO strings (with or without 'Z') ----
    @field_validator("scraped_at", mode="before")
    @classmethod
    def _parse_scraped_at(cls, v):
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v

    # ---- ensure scraped_at is timezone-aware (default UTC) ----
    @model_validator(mode="after")
    def _ensure_tz(self):
        if self.scraped_at.tzinfo is None:
            object.__setattr__(self, "scraped_at", self.scraped_at.replace(tzinfo=timezone.utc))
        return self
