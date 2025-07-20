from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..services.outlet_service import list_outlets, get_outlet
from ..database import get_db
from typing import Optional

router = APIRouter()

@router.get("/outlets")
def get_outlets(
    limit: Optional[int] = Query(None, ge=1, le=1000, description="Limit number of results"),
    offset: Optional[int] = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db)
):
    return list_outlets(db, limit, offset)

@router.get("/outlets/{outlet_id}")
def get_outlet_by_id(outlet_id: int, db: Session = Depends(get_db)):
    outlet = get_outlet(db, outlet_id)
    if not outlet:
        raise HTTPException(status_code=404, detail="Outlet not found")
    return outlet 