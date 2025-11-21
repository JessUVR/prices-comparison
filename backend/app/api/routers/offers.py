from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infra.db.database import get_db
from app.domain.schemas import OfferCreate, OfferUpdate, OfferRead
from app.domain.crud import (
    create_offer,
    get_offer,
    get_all_offers,
    update_offer,
    delete_offer
)

router = APIRouter(prefix="/offers", tags=["Offers"])


@router.post("/", response_model=OfferRead)
def create_offer_endpoint(offer_in: OfferCreate, db: Session = Depends(get_db)):
    return create_offer(db, offer_in)


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer_endpoint(offer_id: int, db: Session = Depends(get_db)):
    offer = get_offer(db, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@router.get("/", response_model=list[OfferRead])
def get_all_offers_endpoint(db: Session = Depends(get_db)):
    return get_all_offers(db)


@router.put("/{offer_id}", response_model=OfferRead)
def update_offer_endpoint(offer_id: int, offer_in: OfferUpdate, db: Session = Depends(get_db)):
    offer = update_offer(db, offer_id, offer_in)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


@router.delete("/{offer_id}")
def delete_offer_endpoint(offer_id: int, db: Session = Depends(get_db)):
    success = delete_offer(db, offer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"message": "Offer deleted successfully"}
