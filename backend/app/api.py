from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, Outlet
import json
from chatbot import router as chatbot_router

app = FastAPI()
"""
Main FastAPI application setup, including CORS and router registration.
"""

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register chatbot router
app.include_router(chatbot_router)

@app.get("/outlets")
def get_outlets(db: Session = Depends(get_db)):
    """
    Get all outlets from the database.
    """
    outlets = db.query(Outlet).all()
    return [
        {
            "id": o.id,
            "name": o.name,
            "address": o.address,
            "operating_hours": o.operating_hours,
            "waze_link": o.waze_link,
            "latitude": o.latitude,
            "longitude": o.longitude,
            "features": json.loads(o.features) if o.features else []
        }
        for o in outlets
    ]

@app.get("/outlets/{outlet_id}")
def get_outlet(outlet_id: int, db: Session = Depends(get_db)):
    """
    Get a single outlet by ID.
    """
    outlet = db.query(Outlet).filter(Outlet.id == outlet_id).first()
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return {
        "id": outlet.id,
        "name": outlet.name,
        "address": outlet.address,
        "operating_hours": outlet.operating_hours,
        "waze_link": outlet.waze_link,
        "latitude": outlet.latitude,
        "longitude": outlet.longitude,
        "features": json.loads(outlet.features) if outlet.features else []
    }
