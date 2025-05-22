# init_db.py
from backend.db.database import Base, engine
from backend.db import models

print("⏳ Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")