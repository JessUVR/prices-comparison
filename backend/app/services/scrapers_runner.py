from sqlalchemy.orm import Session

from scrapers.oxxo import scrape_offers as scrape_offers_oxxo
from scrapers.merco import scrape_offers as scrape_offers_merco
from app.domain.schemas import OfferCreate
from app.domain import crud, models, schemas
from app.infra.db.database import SessionLocal


def run_oxxo_scraper(db: Session) -> int:
    scraped_offers = scrape_offers_oxxo()
    print(f"[DEBUG OXXO] scraped_offers len = {len(scraped_offers)}")

    store = db.query(models.Store).filter(models.Store.name == "OXXO").first()
    if not store:
        print("[ERROR] Store 'OXXO' does NOT exist in table 'stores'.")
        return 0

    # 🔥 DELETE OLD OFFERS FROM THIS STORE
    deleted = crud.delete_offers_by_store(db, store.id)
    print(f"[OXXO] Deleted {deleted} old offers")

    created_count = 0
    for offer in scraped_offers:
        new_offer = OfferCreate(
            store_id=store.id,
            title=offer.title,
            price=offer.price,
            validity_text=offer.validity_text,
            image_url=offer.image_url,
            product_url=offer.product_url,
        )
        crud.create_offer(db, new_offer)
        created_count += 1

    db.commit()
    return created_count


def run_merco_scraper(db: Session) -> int:
    scraped_offers = scrape_offers_merco()
    print(f"[DEBUG MERCO] scraped_offers len = {len(scraped_offers)}")

    store = db.query(models.Store).filter(models.Store.name == "Merco").first()
    if not store:
        print("[ERROR] Store 'MERCO' does NOT exist in table 'stores'.")
        return 0

    # 🔥 DELETE OLD OFFERS FROM THIS STORE
    deleted = crud.delete_offers_by_store(db, store.id)
    print(f"[MERCO] Deleted {deleted} old offers")

    created_count = 0
    for offer in scraped_offers:
        new_offer = OfferCreate(
            store_id=store.id,
            title=offer.title,
            price=offer.price,
            validity_text=offer.validity_text,
            image_url=offer.image_url,
            product_url=offer.product_url,
        )
        crud.create_offer(db, new_offer)
        created_count += 1

    db.commit()
    return created_count


if __name__ == "__main__":
    db = SessionLocal()
    try:
        created_oxxo_offers = run_oxxo_scraper(db)
        created_merco_offers = run_merco_scraper(db)
        print(f"Created {created_oxxo_offers} offers from OXXO")
        print(f"Created {created_merco_offers} offers from MERCO")
    finally:
        db.close()
