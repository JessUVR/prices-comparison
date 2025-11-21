from typing import Optional

from sqlalchemy.orm import Session

from app.domain.models import Offer
from app.domain.schemas import OfferCreate, OfferUpdate


def create_offer(db: Session, offer_in: OfferCreate) -> Offer:
    try:
        db_offer = Offer(**offer_in.model_dump())
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return db_offer
    except:
        db.rollback()
        raise

def get_offer(db: Session, offer_id: int) -> Optional[Offer]:
    return db.get(Offer, offer_id)

def get_all_offers(db: Session) -> list[Offer]:
    return db.query(Offer).all()

def update_offer(db: Session, offer_id: int, offer_in: OfferUpdate) -> Optional[Offer]:
    db_offer = db.get(Offer, offer_id)
    if not db_offer:
        return None

    for key, value in offer_in.model_dump(exclude_unset=True).items():
        setattr(db_offer, key, value)

    try:
        db.add(db_offer)
        db.commit()
        db.refresh(db_offer)
        return db_offer
    except:
        db.rollback()
        raise

def delete_offer(db: Session, offer_id: int) -> bool:
    db_offer = db.get(Offer, offer_id)
    if not db_offer:
        return False

    try:
        db.delete(db_offer)
        db.commit()
        return True
    except:
        db.rollback()
        raise
