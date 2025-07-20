from typing import List, Optional
from sqlalchemy.orm import Session
from ..repositories.outlet_repository import get_all_outlets, get_outlet_by_id, get_outlets_by_features
import json

def list_outlets(db: Session, limit: Optional[int] = None, offset: Optional[int] = 0) -> List[dict]:
    outlets = get_all_outlets(db, limit, offset)
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

def get_outlet(db: Session, outlet_id: int) -> Optional[dict]:
    outlet = get_outlet_by_id(db, outlet_id)
    if not outlet:
        return None
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

def find_outlets_by_features(db: Session, features: List[str]) -> List[dict]:
    outlets = get_outlets_by_features(db, features)
    result = []
    for o in outlets:
        try:
            outlet_features = json.loads(o.features) if o.features else []
        except json.JSONDecodeError:
            outlet_features = []
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