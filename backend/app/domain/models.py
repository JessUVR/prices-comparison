from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.infra.db.database import Base


# STORE MODEL
class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    logo_url = Column(String)
    last_scraped_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One store for many offers
    offers = relationship("Offer", back_populates="store")


# OFFER MODEL
class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float, nullable=True)
    validity_text = Column(String)
    image_url = Column(String)
    store_id = Column(Integer, ForeignKey("stores.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Each offer belongs to one store
    store = relationship("Store", back_populates="offers")
