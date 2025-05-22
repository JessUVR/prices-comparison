from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey
from backend.db.database import Base  # 👈 Make sure to import your Base class

# Product model/table
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    current_price = Column(String, nullable=True)
    original_price = Column(String, nullable=True)
    promotion = Column(String, nullable=True)
    requires_coupon = Column(Boolean, default=False)
    valid_until = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    store = Column(String)
    date = Column(String, nullable=True)

# Offer model/table
class Offer(Base):
    __tablename__ = "offers"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    discount = Column(Float)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
