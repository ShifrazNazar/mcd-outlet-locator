# Frontend: McDonald's Outlet Locator

## Overview

This frontend visualizes McDonald's outlets in Kuala Lumpur on a map, with advanced search and chatbot features, using data from the backend API.

## Setup Instructions

1. **Navigate to the frontend directory:**
   ```sh
   cd frontend
   ```
2. **Install dependencies:**
   ```sh
   yarn install
   # or
   npm install
   ```
3. **Set up environment variables:**
   - Create a `.env` file in `frontend/` with:
     ```
     VITE_API_URL=http://localhost:8000
     ```
4. **Run the frontend dev server:**
   ```sh
   yarn dev
   # or
   npm run dev
   ```
   The app will be available at `http://localhost:5173`.

## Features

- **Map Visualization:** All outlets shown as markers with 5KM radius circles.
- **Intersection Highlighting:** Outlets with overlapping 5KM radii are shown in red.
- **Chatbot Search:** Use the search box to find outlets by features (e.g., "24 hours", "birthday party").

## Chatbot Examples

- **Which outlets in KL operate 24 hours?**
- **Which outlet allows birthday parties?**
- **Show outlets with drive-thru.**
- **Where can I get breakfast in KL?**

## Environment Variables

- `VITE_API_URL` (required): URL of the backend API.

## Dependencies

See `package.json` for full list. Key packages:

- react, react-dom, react-query, react-leaflet, leaflet, react-hook-form, tailwindcss

## Notes

- **No API keys or secrets are committed to the repository.**
- **Tested on Node 18+ and modern browsers.**
