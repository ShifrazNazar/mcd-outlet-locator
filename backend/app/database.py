from sqlalchemy import create_engine, Column, Integer, String, Float, Text, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database connection with PostgreSQL-specific configuration
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # echo=True for debugging SQL queries

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Outlet(Base):
    __tablename__ = "outlets"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    address = Column(Text)
    operating_hours = Column(Text)
    waze_link = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    features = Column(Text)  # Store outlet features as JSON string

# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check function
def check_database_connection():
    """Check if database connection is healthy"""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False