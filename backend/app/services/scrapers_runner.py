# app/services/scrapers_runner.py

from sqlalchemy.orm import Session

from scrapers.oxxo import scrape_offers
from app.domain.schemas import OfferCreate
from app.domain import crud, models
from app.infra.db.database import SessionLocal


def run_oxxo_scraper(db: Session) -> int:
    scraped_offers = scrape_offers()
    print(f"[DEBUG] Scraper returned {len(scraped_offers)} offers")

    created_count = 0

    store = db.query(models.Store).filter(models.Store.name == "OXXO").first()
    if not store:
        print("[ERROR] Store 'OXXO' does NOT exist in table 'stores'.")
        return 0

    for offer in scraped_offers:
        new_offer = OfferCreate(
            store_id=store.id,
            title=offer.title,
            price=offer.price,
            validity_text=offer.validity_text,
            image_url=offer.image_url,
        )

        crud.create_offer(db, new_offer)
        created_count += 1

    db.commit()
    return created_count


if __name__ == "__main__":
    db = SessionLocal()
    try:
        created = run_oxxo_scraper(db)
        print(f"Created {created} offers from OXXO")
    finally:
        db.close()
