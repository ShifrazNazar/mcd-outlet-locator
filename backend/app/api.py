from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db, Outlet
import json

app = FastAPI()

@app.get("/outlets")
def get_outlets(db: Session = Depends(get_db)):
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
