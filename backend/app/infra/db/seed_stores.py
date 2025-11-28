from app.infra.db.database import SessionLocal
from app.domain import models

def get_or_create_store(db, name: str, url: str, logo_url: str = "") -> models.Store:
    """Busca una tienda por nombre; si no existe, la crea."""
    store = db.query(models.Store).filter(models.Store.name == name).first()
    if store:
        print(f"Store '{name}' already exists with id={store.id}")
        return store

    store = models.Store(
        name=name,
        url=url,
        logo_url=logo_url,
    )
    db.add(store)
    db.commit()
    db.refresh(store)
    print(f"Created store '{name}' with id={store.id}")
    return store


def seed_stores() -> None:
    """Crea las tiendas base necesarias para el prototipo."""
    db = SessionLocal()
    try:
        # OXXO
        get_or_create_store(
            db,
            name="OXXO",
            url="https://www.oxxo.com",
        )

        # Soriana
        get_or_create_store(
            db,
            name="Soriana",
            url="https://www.soriana.com",
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed_stores()
