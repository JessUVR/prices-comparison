from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Database URL - points to the SQLite file
DATABASE_URL = "sqlite:///./offers.db"

# Create the database engine - establishes the connection
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# Session factory - creates database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models
Base = declarative_base()

# Dependency for FastAPI - provides a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()