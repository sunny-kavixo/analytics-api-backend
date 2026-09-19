# Analytics API Backend

Production-style analytics REST API built with **FastAPI, SQLAlchemy, PostgreSQL, Docker and SQL analytics**.

## Features
- Validated event ingestion
- PostgreSQL persistence with SQLite fallback
- Event listing
- SQL aggregation: event count, unique users, total and average value
- Docker Compose environment
- Pytest API tests
- GitHub Actions CI
- Interactive OpenAPI documentation at `/docs`

## Architecture
```
Client -> FastAPI -> SQLAlchemy -> PostgreSQL
                    |
                    -> SQL analytics
```

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run with PostgreSQL
```bash
docker compose up --build
```

## Endpoints
- `GET /health`
- `POST /events`
- `GET /events?limit=50`
- `GET /analytics/summary`

## Tests
```bash
pytest -q
```

Uses synthetic/example data only; no private customer data is included.
