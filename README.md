# Prices Comparison – Alcohol Offers

Full-stack project focused on collecting, normalizing, and displaying alcohol offers from different retail stores.

The project emphasizes **backend architecture**, **data scraping**, and **clean data handling**, with a simple frontend used as a visualization layer.

---

## Demo

Short video showing browsing offers and opening the offer details modal.

https://github.com/user-attachments/assets/6fae15a7-ce35-4ba2-8144-8f5996f69388

---

## Features

- Scrapers for multiple retail stores
- Data normalization and validation
- REST API built with FastAPI
- Responsive frontend built with React
- Offer details modal
- Unit tests for core business logic

---

## Tech Stack

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite
- Web scraping utilities
- Unit tests (script-style)

### Frontend
- React
- Vite
- Tailwind CSS

---

## Project Structure

```text
prices-comparison/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── infra/
│   │   ├── services/
│   │   └── tests/
│   └── scrapers/
├── frontend/
│   └── src/
└── README.md
