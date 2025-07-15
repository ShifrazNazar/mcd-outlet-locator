import requests
from database import SessionLocal, Outlet
import time

def geocode_address(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'limit': 1
    }
    response = requests.get(url, params=params, headers={"User-Agent": "mcd-geocoder/1.0"})
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None, None

def geocode_outlets():
    db = SessionLocal()
    try:
        outlets = db.query(Outlet).filter((Outlet.latitude == None) | (Outlet.longitude == None)).all()
        for outlet in outlets:
            lat, lon = geocode_address(outlet.address)
            if lat and lon:
                outlet.latitude = lat
                outlet.longitude = lon
                print(f"✅ Geocoded: {outlet.name} -> ({lat}, {lon})")
            else:
                print(f"❌ Failed to geocode: {outlet.name}")
            db.commit()
            time.sleep(1)  # Be polite to the API
    finally:
        db.close()

if __name__ == "__main__":
    geocode_outlets()
