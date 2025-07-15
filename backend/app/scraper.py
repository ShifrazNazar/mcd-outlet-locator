from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import re
from database import SessionLocal, Outlet, create_tables

class McDonaldsScraper:
    def __init__(self):
        self.base_url = "https://www.mcdonalds.com.my/locate-us"
        self.driver = None
        self.db = SessionLocal()
        
    def setup_driver(self):
        """Setup Chrome driver with options"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Remove this to see the browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)
        
    def filter_by_kuala_lumpur(self):
        """Filter search results by Kuala Lumpur using the state dropdown"""
        try:
            print("🔍 Filtering by Kuala Lumpur...")
            time.sleep(3)  # Wait for page to load

            # Find the state dropdown by id 'states'
            state_select = self.driver.find_element(By.ID, "states")
            for option in state_select.find_elements(By.TAG_NAME, 'option'):
                if option.text.strip().lower() == "kuala lumpur":
                    option.click()
                    break
            time.sleep(2)

            # Click the search button (id 'search-now')
            search_button = self.driver.find_element(By.ID, "search-now")
            search_button.click()
            time.sleep(5)
            print("✅ Filtered by Kuala Lumpur using dropdown")
        except Exception as e:
            print(f"⚠️ Could not filter by KL using dropdown: {e}")
            
    def extract_outlet_data(self, outlet_element):
        """Extract data from a single outlet element"""
        try:
            # Get the HTML content
            html = outlet_element.get_attribute('outerHTML')
            soup = BeautifulSoup(html, 'html.parser')
            
            # First, try to extract from JSON-LD script tag
            json_script = soup.find('script', type='application/ld+json')
            if json_script:
                import json
                try:
                    data = json.loads(json_script.string)
                    name = data.get('name', '')
                    address = data.get('address', '')
                    geo = data.get('geo', {})
                    latitude = geo.get('latitude')
                    longitude = geo.get('longitude')

                    # Always generate Waze link using latitude and longitude
                    waze_link = ""
                    if latitude is not None and longitude is not None:
                        waze_link = f"https://www.waze.com/live-map/directions?navigate=yes&to=ll.{latitude},{longitude}"
                    
                    # Extract all feature texts
                    feature_elements = soup.find_all('span', class_='ed-tooltiptext')
                    features = [el.get_text(strip=True) for el in feature_elements if el.get_text(strip=True)]
                    
                    # Extract operating hours from features
                    operating_hours = "Unknown"
                    for feature in features:
                        if "24 hour" in feature.lower():
                            operating_hours = "24 Hours"
                            break
                    if operating_hours != "24 Hours":
                        operating_hours = "6am - 2am"
                    
                    return {
                        'name': name,
                        'address': address,
                        'operating_hours': operating_hours,
                        'waze_link': waze_link,
                        'latitude': latitude,
                        'longitude': longitude,
                        'features': json.dumps(features)
                    }
                except json.JSONDecodeError:
                    pass
            
        except Exception as e:
            print(f"⚠️ Error extracting outlet data: {e}")
            return None
            
    def scrape_current_page(self):
        """Scrape outlets from current page"""
        outlets = []
        
        try:
            # Wait for page to load
            time.sleep(3)
            
            # Look for the results container
            results_container = self.driver.find_element(By.ID, "results")
            
            # Find all outlet boxes - they have class "addressBox"
            outlet_elements = results_container.find_elements(By.CLASS_NAME, "addressBox")
            
            
            print(f"📍 Found {len(outlet_elements)} outlets on this page")
            
            for i, element in enumerate(outlet_elements):
                outlet_data = self.extract_outlet_data(element)
                if outlet_data and outlet_data['name'] != "Unknown" and len(outlet_data['name']) > 3:
                    outlets.append(outlet_data)
                    print(f"  ✅ {outlet_data['name']} - {outlet_data['address'][:50]}...")
                else:
                    print(f"  ⚠️ Skipped element {i+1} (insufficient data)")
                    
        except Exception as e:
            print(f"❌ Error scraping current page: {e}")
            
        return outlets
    
    def handle_pagination(self):
        """Handle pagination to get all pages"""
        all_outlets = []
        page_num = 1
        
        while True:
            print(f"\n📄 Scraping page {page_num}...")
            
            # Scrape current page
            outlets = self.scrape_current_page()
            all_outlets.extend(outlets)
            
            # Look for next button
            try:
                next_selectors = [
                    ".pagination-next", ".next", ".btn-next", 
                    "[class*='next']", "[aria-label*='next']",
                    "button[aria-label*='Next']", "a[aria-label*='Next']"
                ]
                
                next_button = None
                for selector in next_selectors:
                    try:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        break
                    except:
                        continue
                
                if next_button and next_button.is_enabled():
                    next_button.click()
                    time.sleep(3)  # Wait for page to load
                    page_num += 1
                else:
                    print("📄 No more pages")
                    break
                    
            except Exception as e:
                print(f"📄 No next button found or pagination complete: {e}")
                break
                
        return all_outlets
        
    def save_to_database(self, outlets):
        """Save outlets to database"""
        try:
            print(f"\n💾 Saving {len(outlets)} outlets to database...")
            
            for outlet_data in outlets:
                # Check if outlet already exists
                existing = self.db.query(Outlet).filter(
                    Outlet.name == outlet_data['name'],
                    Outlet.address == outlet_data['address']
                ).first()
                
                if not existing:
                    outlet = Outlet(
                        name=outlet_data['name'],
                        address=outlet_data['address'],
                        operating_hours=outlet_data['operating_hours'],
                        waze_link=outlet_data['waze_link'],
                        latitude=outlet_data.get('latitude'),
                        longitude=outlet_data.get('longitude'),
                        features=outlet_data.get('features')
                    )
                    self.db.add(outlet)
                    print(f"  ✅ Added: {outlet_data['name']}")
                else:
                    # Update existing outlet with new data if available
                    updated = False
                    if outlet_data.get('latitude') is not None and outlet_data.get('longitude') is not None:
                        existing.latitude = outlet_data['latitude']
                        existing.longitude = outlet_data['longitude']
                        updated = True
                    if outlet_data.get('operating_hours') is not None:
                        existing.operating_hours = outlet_data['operating_hours']
                        updated = True
                    if outlet_data.get('waze_link') is not None:
                        existing.waze_link = outlet_data['waze_link']
                        updated = True
                    if outlet_data.get('features') is not None:
                        existing.features = outlet_data['features']
                        updated = True
                    if updated:
                        print(f"  🔄 Updated: {outlet_data['name']}")
                    else:
                        print(f"  ⚠️ Skipped (exists, no new data): {outlet_data['name']}")
                    
            self.db.commit()
            print("✅ All outlets saved to database!")
            
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
            self.db.rollback()
            
    def scrape(self):
        """Main scraping method"""
        try:
            print("🚀 Starting McDonald's outlet scraper...")
            
            # Setup
            create_tables()
            self.setup_driver()
            
            # Navigate to page
            print(f"🌐 Navigating to {self.base_url}")
            self.driver.get(self.base_url)
            
            # Filter by KL
            self.filter_by_kuala_lumpur()
            
            # Scrape all pages
            outlets = self.handle_pagination()
            
            # Save to database
            self.save_to_database(outlets)
            
            print(f"\n🎉 Scraping complete! Found {len(outlets)} outlets total.")
            
        except Exception as e:
            print(f"❌ Scraping failed: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()
            self.db.close()

def main():
    scraper = McDonaldsScraper()
    scraper.scrape()

if __name__ == "__main__":
    main()