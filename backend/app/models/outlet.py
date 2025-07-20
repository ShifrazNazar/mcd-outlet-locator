from sqlalchemy import Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base

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