from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db import crud, models, schemas, database
from backend.scrapers import oxxo, soriana_promos

router = APIRouter()

# 🔧 Dependency to get a DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 📄 List all offers
@router.get("/", response_model=list[schemas.Offer])
def list_offers(db: Session = Depends(get_db)):
    return crud.get_all_offers(db)


# 🔍 Get an offer by ID
@router.get("/{offer_id}", response_model=schemas.Offer)
def get_offer(offer_id: int, db: Session = Depends(get_db)):
    return crud.get_offer_by_id(db, offer_id)


# ➕ Create a new offer
@router.post("/", response_model=schemas.Offer)
def create_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    return crud.create_offer(db, offer)


# 🔁 Replace all offers manually
@router.post("/replace")
def replace_all_offers(offers: list[schemas.OfferCreate], db: Session = Depends(get_db)):
    crud.replace_offers(db, offers)
    return {"message": "Offers replaced successfully ✅"}


# 🤖 Replace all offers from a scraper
@router.post("/load-from-scraper/{store}")
def load_offers_from_scraper(store: str, db: Session = Depends(get_db)):
    if store == "oxxo":
        promotions = oxxo.run()
    elif store == "soriana":
        promotions = soriana_promos.run()
    else:
        return {"error": "Unsupported store"}

    return crud.load_offers_from_scraper(db, promotions)


# 🧹 Delete all offers without replacing
@router.delete("/clear")
def clear_all_offers(db: Session = Depends(get_db)):
    db.query(models.Offer).delete()
    db.commit()
    return {"message": "All offers have been deleted ✅"}
