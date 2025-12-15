# backend/app/main.py
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from app.api.routers.offers import router as offers_router

app = FastAPI(title="Offers API")

app.include_router(offers_router)

origins = [
    "http://localhost:5173",  # Vite
    "http://localhost:3000",  # React CRA
    "http://192.168.1.142:5173",   # Vite Network on your machine
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Use ["*"] to allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Offers API is running"}

