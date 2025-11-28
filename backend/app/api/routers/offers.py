from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.infra.db.database import get_db
from app.domain import models, schemas, crud
from app.services.scrapers_runner import run_oxxo_scraper
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


@router.get("/", response_model=list[OfferRead])
def get_all_offers_endpoint(db: Session = Depends(get_db)):
    return get_all_offers(db)


# ⬇️⬇️⬇️ PRIMERO los endpoints "fijos" como /oxxo


@router.post("/oxxo/scrape")
def scrape_oxxo_offers(db: Session = Depends(get_db)):
    created = run_oxxo_scraper(db)
    return {"created": created}


@router.get("/oxxo", response_model=List[schemas.OfferRead])
def list_oxxo_offers(db: Session = Depends(get_db)):
    store = db.query(models.Store).filter(models.Store.name == "OXXO").first()
    if not store:
        return []
    offers = crud.get_offers_by_store(db, store_id=store.id)
    return offers


@router.delete("/clear-all")
def delete_all_offers_endpoint(db: Session = Depends(get_db)):
    deleted = crud.delete_all_offers(db)
    return {"deleted": deleted}


# ⬇️⬇️⬇️ HASTA EL FINAL el que tiene path param {offer_id}


@router.get("/{offer_id}", response_model=OfferRead)
def get_offer_endpoint(offer_id: int, db: Session = Depends(get_db)):
    offer = get_offer(db, offer_id)
    if not offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return offer


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
