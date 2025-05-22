from sqlalchemy.orm import Session
from backend.db import models, schemas
from backend.utils.helpers import clean_text


# ✅ Create a new offer manually
def create_offer(db: Session, offer: schemas.OfferCreate):
    new_offer = models.Offer(
        description=clean_text(offer.description),
        discount=offer.discount
    )
    db.add(new_offer)
    db.commit()
    db.refresh(new_offer)
    return new_offer


# ✅ Get all offers
def get_all_offers(db: Session):
    return db.query(models.Offer).all()


# ✅ Get offer by ID
def get_offer_by_id(db: Session, offer_id: int):
    return db.query(models.Offer).filter(models.Offer.id == offer_id).first()


# ✅ Replace all offers manually
def replace_offers(db: Session, offers: list[schemas.OfferCreate]):
    db.query(models.Offer).delete()
    db.commit()
    for offer in offers:
        create_offer(db, offer)


# ✅ Load offers from scraper (OXXO or Soriana)
def load_offers_from_scraper(db: Session, promotions: list[dict]):
    db.query(models.Offer).delete()
    db.commit()
    for promo in promotions:
        offer = models.Offer(
            description=clean_text(promo.get("description", "")),
            discount=promo.get("discount", 0.0)
        )
        db.add(offer)
        db.commit()
    return {"message": "Offers loaded from scraper ✅"}
