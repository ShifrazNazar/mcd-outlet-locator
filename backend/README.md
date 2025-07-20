# Backend: McDonald's Outlet Locator

## Overview

This backend scrapes McDonald's outlets in Kuala Lumpur, stores them in a database, geocodes their addresses, and exposes a FastAPI API for frontend and chatbot use.

---

## Architecture (Layered Structure)

The backend is organized using a **Layered Architecture** for maintainability and scalability:

- **main.py**: Entrypoint for running the server (with Uvicorn).
- **api.py**: Assembles the FastAPI app, configures middleware, and includes routers.
- **database.py**: Sets up the database engine, session, and DB utilities.
- **models/**: Contains SQLAlchemy models (e.g., `models/outlet.py`).
- **repositories/**: Data access layer (e.g., `repositories/outlet_repository.py`).
- **services/**: Business logic layer (e.g., `services/outlet_service.py`, `services/chatbot_service.py`).
- **api/**: API routers/controllers (e.g., `api/outlet.py`, `api/chatbot.py`).

**Scripts** like `scraper.py`, `geocoding.py`, and `migration_script.py` use the new structure and import from the appropriate layers.

**Example Directory Structure:**

```
backend/app/
  main.py           # Entrypoint (runs the server)
  api.py            # FastAPI app, routers, middleware
  database.py       # DB engine/session/utilities
  models/
    outlet.py       # SQLAlchemy Outlet model
  repositories/
    outlet_repository.py  # Data access for outlets
  services/
    outlet_service.py     # Business logic for outlets
    chatbot_service.py    # Business logic for chatbot
  api/
    outlet.py       # Outlet API endpoints
    chatbot.py      # Chatbot API endpoint
    __init__.py     # Router includes
  scraper.py        # Web scraper for outlets
  geocoding.py      # Geocoding script
  migration_script.py # SQLite to PostgreSQL migration
```

---

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd backend
   ```
2. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in `backend/app/` with:
     ```
     DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<dbname>
     # or for SQLite (for local dev):
     # DATABASE_URL=sqlite:///outlets.db
     GEMINI_API_KEY=your_gemini_api_key  # (optional, for chatbot LLM)
     ```
5. **Initialize the database:**
   ```sh
   python -m app.main
   ```
   This will create tables and verify the connection.
6. **Run the backend server:**
   ```sh
   uvicorn app.main:app --reload
   ```
   The API will be available at `http://localhost:8000`.

---

## Usage

### Running the Scraper

```sh
python -m app.scraper
```

This will scrape all KL outlets and store them in the database.

### Geocoding Outlets

```sh
python -m app.geocoding
```

This will fill in latitude/longitude for outlets missing coordinates.

### API Endpoints

- `GET /outlets`: List all outlets (supports `limit` and `offset`).
- `GET /outlets/{id}`: Get details for a specific outlet.
- `POST /chatbot`: Query outlets by features (see Chatbot Examples).
- `GET /health`: Health check.

---

## Environment Variables

- `DATABASE_URL` (required): PostgreSQL or SQLite connection string.
- `GEMINI_API_KEY` (optional): For Google Gemini LLM-powered chatbot.

---

## Dependencies

See `requirements.txt` for full list. Key packages:

- fastapi, sqlalchemy, uvicorn, requests, selenium, python-dotenv, google-genai, psycopg2-binary

---

## Notes

- **No API keys or secrets are committed to the repository.**
- **Gemini LLM is optional:** If not set, chatbot falls back to keyword search.
- **Geocoding uses OpenStreetMap Nominatim:** Be mindful of rate limits.
- **Tested on Python 3.8+.**
