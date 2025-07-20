# MindHive Technical Assessment: McDonald's Outlet Locator

## Project Overview

This project scrapes McDonald's outlets in Kuala Lumpur, stores them in a database, geocodes their addresses, exposes a FastAPI backend, and provides a React frontend to visualize outlets on a map with advanced search and chatbot features.

## Architecture & Key Decisions

- **Backend:** Python 3.8+, FastAPI, SQLAlchemy, PostgreSQL (or SQLite for local dev), Selenium for scraping, OpenStreetMap Nominatim for geocoding, Google Gemini LLM (optional) for chatbot.
- **Frontend:** React (Vite + TypeScript), React Query for data fetching, React Leaflet for mapping, TailwindCSS for styling.
- **Why these choices?**
  - **FastAPI:** Modern, async, easy OpenAPI docs, great for rapid prototyping.
  - **React + Vite:** Fast dev experience, modern tooling, easy integration with mapping libraries.
  - **Selenium:** Handles dynamic web pages and pagination.
  - **OpenStreetMap:** Free, no API key required for geocoding.
  - **Gemini LLM:** Demonstrates agentic/LLM search, but falls back to keyword search if unavailable.

## Getting Started

- **Backend:** See [`backend/README.md`](backend/README.md) for setup, usage, and API details.
- **Frontend:** See [`frontend/README.md`](frontend/README.md) for setup, usage, and features.
