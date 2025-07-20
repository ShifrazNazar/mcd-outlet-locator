from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.outlet import Outlet
import json

def get_all_outlets(db: Session, limit: Optional[int] = None, offset: Optional[int] = 0) -> List[Outlet]:
    query = db.query(Outlet)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    return query.all()

def get_outlet_by_id(db: Session, outlet_id: int) -> Optional[Outlet]:
    return db.query(Outlet).filter(Outlet.id == outlet_id).first()

def get_outlets_by_features(db: Session, features: List[str]) -> List[Outlet]:
    outlets = db.query(Outlet).all()
    result = []
    for o in outlets:
        try:
            outlet_features = json.loads(o.features) if o.features else []
        except json.JSONDecodeError:
            outlet_features = []
        if any(f in outlet_features for f in features):
            result.append(o)
    return result 