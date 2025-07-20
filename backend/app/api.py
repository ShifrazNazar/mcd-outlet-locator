from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db, Outlet, check_database_connection
import json
from typing import List, Optional
from .chatbot import router as chatbot_router

app = FastAPI(
    title="McDonald's Outlet Locator API",
    description="API for finding McDonald's outlets with geospatial capabilities",
    version="1.0.0"
)

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

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "message": "McDonald's Outlet Locator API",
        "version": "1.0.0",
        "database": "connected" if check_database_connection() else "disconnected"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    db_status = check_database_connection()
    return {
        "status": "healthy" if db_status else "unhealthy",
        "database": "connected" if db_status else "disconnected"
    }

@app.get("/outlets")
def get_outlets(
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit number of results"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    """
    Get all outlets from the database with optional pagination.
    """
    query = db.query(Outlet)
    
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    
    outlets = query.all()
    
    result = []
    for o in outlets:
        try:
            features = json.loads(o.features) if o.features else []
        except json.JSONDecodeError:
            features = []
        
        result.append({
            "id": o.id,
            "name": o.name,
            "address": o.address,
            "operating_hours": o.operating_hours,
            "waze_link": o.waze_link,
            "latitude": o.latitude,
            "longitude": o.longitude,
            "features": features
        })
    
    return result

@app.get("/outlets/{outlet_id}")
def get_outlet(outlet_id: int, db: Session = Depends(get_db)):
    """
    Get a single outlet by ID.
    """
    outlet = db.query(Outlet).filter(Outlet.id == outlet_id).first()
    
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    
    try:
        features = json.loads(outlet.features) if outlet.features else []
    except json.JSONDecodeError:
        features = []
    
    return {
        "id": outlet.id,
        "name": outlet.name,
        "address": outlet.address,
        "operating_hours": outlet.operating_hours,
        "waze_link": outlet.waze_link,
        "latitude": outlet.latitude,
        "longitude": outlet.longitude,
        "features": features
    }