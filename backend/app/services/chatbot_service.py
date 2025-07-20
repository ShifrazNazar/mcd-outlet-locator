import os
import re
import json
from typing import List
from ..services.outlet_service import find_outlets_by_features
from google import genai

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

def extract_features_simple(query: str) -> List[str]:
    query_lower = query.lower()
    matched_features = []
    if "24" in query_lower or "hour" in query_lower:
        matched_features.append("24 Hours")
    if "birthday" in query_lower or "party" in query_lower:
        matched_features.append("Birthday Party")
    if "breakfast" in query_lower:
        matched_features.append("Breakfast")
    if "cashless" in query_lower or "card" in query_lower or "payment" in query_lower:
        matched_features.append("Cashless Facility")
    if "dessert" in query_lower:
        matched_features.append("Dessert Center")
    if "kiosk" in query_lower or "digital" in query_lower:
        matched_features.append("Digital Order Kiosk")
    if "drive" in query_lower or "thru" in query_lower:
        matched_features.append("Drive-Thru")
    if "cafe" in query_lower or "coffee" in query_lower:
        matched_features.append("McCafe")
    if "delivery" in query_lower:
        matched_features.append("McDelivery")
    if "wifi" in query_lower or "internet" in query_lower:
        matched_features.append("WiFi")
    return matched_features

def extract_features_with_gemini(query: str) -> List[str]:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return extract_features_simple(query)
    try:
        client = genai.Client(api_key=api_key)
        prompt = f"""
You are an assistant for a McDonald's outlet search. Given a user query, extract which of the following features are being asked about (if any):
{', '.join(KNOWN_FEATURES)}

User query: '{query}'

Return a JSON array of the relevant features from the list above that match the user's intent. Only include features from the list. If none match, return an empty array.
"""
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        text = getattr(response, 'text', None)
        if not text:
            return extract_features_simple(query)
        match = re.search(r'\[.*?\]', text, re.DOTALL)
        if match:
            features = json.loads(match.group(0))
            if isinstance(features, list):
                return [f for f in features if f in KNOWN_FEATURES]
        return extract_features_simple(query)
    except Exception:
        return extract_features_simple(query)

def chatbot_search(db, query: str):
    features = extract_features_with_gemini(query)
    if features:
        result = find_outlets_by_features(db, features)
        return {"outlets": result, "matched_features": features, "source": "llm"}
    else:
        return {"outlets": [], "matched_features": [], "source": "llm"} 