from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends

# 1. Database URL (we are using SQLite for now)
SQLALCHEMY_DATABASE_URL = "sqlite:///./products.db"

# 2. Create database engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # only applies to SQLite
)

# 3. Create local session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Create base class for models
Base = declarative_base()

# 5. Dependency to get a DB session per request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
