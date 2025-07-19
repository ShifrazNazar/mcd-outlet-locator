import os
import re
import json
from typing import List
from fastapi import APIRouter, HTTPException, Request, Depends
from sqlalchemy.orm import Session
from .database import get_db, Outlet
from google import genai

router = APIRouter()

KNOWN_FEATURES = [
    "24 Hours",
    "Birthday Party",
    "Breakfast",
    "Cashless Facility",
    "Dessert Center",
    "Digital Order Kiosk",
    "Drive-Thru",
    "McCafe",
    "McDelivery",
    "WiFi"
]

def extract_features_with_gemini(query: str) -> List[str]:
    """
    Use Gemini LLM to extract relevant features from a user query.
    Returns a list of features from KNOWN_FEATURES that match the user's intent.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    client = genai.Client(api_key=api_key)
    prompt = f"""
You are an assistant for a McDonald's outlet search. Given a user query, extract which of the following features are being asked about (if any):
{', '.join(KNOWN_FEATURES)}

User query: '{query}'

Return a JSON array of the relevant features from the list above that match the user's intent. Only include features from the list. If none match, return an empty array.
"""
    try:
        print("[Gemini LLM] Input prompt:")
        print(prompt)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print("[Gemini LLM] Raw response:")
        print(response)
        text = getattr(response, 'text', None)
        if not text:
            return []
        print("[Gemini LLM] Response text:")
        print(text)
        match = re.search(r'\[.*?\]', text, re.DOTALL)
        if match:
            features = json.loads(match.group(0))
            if isinstance(features, list):
                return [f for f in features if f in KNOWN_FEATURES]
        return []
    except Exception as e:
        print(f"[Gemini LLM] Error: {e}")
        return []

def get_outlets_by_features(db: Session, features: List[str]) -> List[dict]:
    """
    Query the database for outlets that have any of the specified features.
    Returns a list of outlet dicts.
    """
    outlets = db.query(Outlet).all()
    result = []
    for o in outlets:
        outlet_features = json.loads(o.features) if o.features else []
        if any(f in outlet_features for f in features):
            result.append({
                "id": o.id,
                "name": o.name,
                "address": o.address,
                "operating_hours": o.operating_hours,
                "waze_link": o.waze_link,
                "latitude": o.latitude,
                "longitude": o.longitude,
                "features": outlet_features
            })
    return result

@router.post("/chatbot")
async def chatbot_search(request: Request, db: Session = Depends(get_db)):
    """
    Chatbot endpoint: Accepts a user query, extracts features using Gemini LLM,
    and returns outlets matching those features.
    """
    data = await request.json()
    query = data.get("query", "")
    print(f"[Chatbot] Incoming query: {query}")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    features = extract_features_with_gemini(query)
    print(f"[Chatbot] Extracted features: {features}")
    if features:
        result = get_outlets_by_features(db, features)
        print(f"[Chatbot] Matching outlets: {len(result)}")
        return {"outlets": result, "matched_features": features, "source": "llm"}
    else:
        print("[Chatbot] No features matched. Returning empty result.")
        return {"outlets": [], "matched_features": [], "source": "llm"}
