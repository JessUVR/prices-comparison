from app.infra.db.database import engine
from app.domain.models import Base

def main():
    """creates database tables"""
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    main()
