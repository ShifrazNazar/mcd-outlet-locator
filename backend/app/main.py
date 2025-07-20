import uvicorn
import os
from .api import app
from .database import create_tables, check_database_connection

def initialize_database():
    """Initialize database tables and extensions"""
    print("Initializing database...")
    try:
        create_tables()
        print("✓ Database tables created successfully")
        
        if check_database_connection():
            print("✓ Database connection verified")
        else:
            print("✗ Database connection failed")
            return False
            
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("Starting McDonald's Outlet Locator API...")
    print(f"Database URL: {os.getenv('DATABASE_URL', 'Not set')[:50]}...")
    
    # Initialize database before starting the server
    if initialize_database():
        print("🚀 Starting server on http://0.0.0.0:8000")
        uvicorn.run(
            app, 
            host="0.0.0.0", 
            port=int(os.getenv("PORT", 8000)),
            reload=os.getenv("ENVIRONMENT") == "development"
        )
    else:
        print("❌ Server startup cancelled due to database initialization failure")
        exit(1)