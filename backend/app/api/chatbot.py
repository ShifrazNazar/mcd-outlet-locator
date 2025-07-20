from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from ..services.chatbot_service import chatbot_search
from ..database import get_db

router = APIRouter()

@router.post("/chatbot")
async def chatbot_endpoint(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
        query = data.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        return chatbot_search(db, query)
    except Exception as e:
        return {"outlets": [], "matched_features": [], "source": "error", "error": str(e)} 