# CMTA Metro Bus — Backend Setup

## Prerequisites
- Python 3.11+
- PostgreSQL running locally

## First-time setup

```bash
# 1. Navigate to backend folder
cd D:\HCI-Final\backend

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create your .env file
copy .env.example .env
# Then open .env and fill in your PostgreSQL password and OpenRouter key

# 5. Create the database in PostgreSQL
# Open psql or pgAdmin and run:
# CREATE DATABASE cmta_db;

# 6. Seed the database with real CMTA data
python -m app.seed_data

# 7. Run the server
uvicorn app.main:app --reload --port 8000
```

## API is live at
- http://localhost:8000          → serves frontend
- http://localhost:8000/docs     → Swagger UI (auto-generated)
- http://localhost:8000/api/lines
- http://localhost:8000/api/stations?line=orange
- http://localhost:8000/api/fare?from_id=1&to_id=8
- http://localhost:8000/api/timings
- http://localhost:8000/api/alerts
- POST http://localhost:8000/api/ai/chat
- POST http://localhost:8000/api/ai/route

## Project structure
```
backend/
├── app/
│   ├── main.py         FastAPI entry point
│   ├── config.py       Settings from .env
│   ├── database.py     PostgreSQL connection
│   ├── models.py       SQLAlchemy ORM models
│   ├── schemas.py      Pydantic request/response schemas
│   ├── seed_data.py    Real CMTA data seed
│   └── routers/
│       ├── routes.py   Lines + stations endpoints
│       ├── fares.py    Fare calculator endpoint
│       ├── alerts.py   Alerts + timings endpoints
│       └── ai.py       OpenRouter AI chat + route finder
├── requirements.txt
├── .env.example
└── README.md
```
