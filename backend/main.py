from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import products, scraper, offers

app = FastAPI()

# Configure CORS to allow requests from the frontend (e.g., React at http://localhost:5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust if using a different port or domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Temporary test route
@app.get("/")
def read_root():
    return {"message": "API is working properly ✅"}

# Include routers
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(scraper.router, prefix="/scraper", tags=["scraper"])
app.include_router(offers.router, prefix="/offers", tags=["offers"])
