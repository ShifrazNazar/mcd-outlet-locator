import uvicorn
import os
from app.api import app

if __name__ == "__main__":
    print("Starting McDonald's Outlet Locator API...")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")
    print("🚀 Starting server on http://0.0.0.0:8000")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )