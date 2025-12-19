from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.infra.db.database import get_db
from app.domain import crud, models
from app.domain.schemas import OfferCreate, OfferUpdate, OfferRead
from app.services.scrapers_runner import run_oxxo_scraper, run_merco_scraper

router = APIRouter(prefix="/offers", tags=["offers"])


# CRUD endpoints (manual)

@router.post("/", response_model=OfferRead)
def create_offer(offer: OfferCreate, db: Session = Depends(get_db)):
    """Create a new offer manually."""
    return crud.create_offer(db=db, offer_in=offer)


@router.get("/", response_model=List[OfferRead])
def read_offers(db: Session = Depends(get_db)):
    """Return all offers."""
    return crud.get_offers(db=db)


@router.get("/{offer_id}", response_model=OfferRead)
def read_offer(offer_id: int, db: Session = Depends(get_db)):
    """Return a single offer by ID."""
    db_offer = crud.get_offer(db=db, offer_id=offer_id)
    if not db_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return db_offer


@router.put("/{offer_id}", response_model=OfferRead)
def update_offer(offer_id: int, offer: OfferUpdate, db: Session = Depends(get_db)):
    """Update an existing offer by ID."""
    db_offer = crud.update_offer(db=db, offer_id=offer_id, offer_in=offer)
    if not db_offer:
        raise HTTPException(status_code=404, detail="Offer not found")
    return db_offer


@router.delete("/{offer_id}")
def delete_offer(offer_id: int, db: Session = Depends(get_db)):
    """Delete an offer by ID."""
    success = crud.delete_offer(db=db, offer_id=offer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Offer not found")
    return {"detail": "Offer deleted successfully"}

@router.delete("/", tags=["offers"])
def delete_all_offers_endpoint(db: Session = Depends(get_db)):
    """
    Delete ALL offers from the database.
    ⚠️ Use only for testing/dev!
    """
    deleted = crud.delete_all_offers(db)
    return {"detail": f"Deleted {deleted} offers"}


# Store-based scraper endpoint

@router.get("/store/{store_slug}", response_model=List[OfferRead])
def get_offers_by_store(store_slug: str, db: Session = Depends(get_db)):
    """
    Return offers for a specific store.

    Supported:
    - 'oxxo'
    - 'merco'
    """
    normalized_slug = store_slug.lower().strip()

    # Map slug -> store name + run scraper
    if normalized_slug == "oxxo":
        store_name = "OXXO"
        run_oxxo_scraper(db=db)     
    elif normalized_slug == "merco":
        store_name = "Merco"
        run_merco_scraper(db=db)   
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Store '{store_slug}' is not supported yet",
        )

    # Find the store in the DB
    store = (
        db.query(models.Store)
        .filter(models.Store.name == store_name)
        .first()
    )
    if not store:
        raise HTTPException(
            status_code=404,
            detail=f"Store '{store_name}' not found in database",
        )

    # Return ONLY its offers
    offers = crud.get_offers_by_store(db=db, store_id=store.id)
    return offers

