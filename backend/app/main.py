# backend/app/main.py

from fastapi import FastAPI
from app.api.routers.offers import router as offers_router

app = FastAPI(title="Offers API")

app.include_router(offers_router)


@app.get("/")
def read_root():
    return {"message": "Offers API is running"}

