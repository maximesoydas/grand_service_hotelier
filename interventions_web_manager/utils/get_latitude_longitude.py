from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import requests_cache

requests_cache.install_cache('geopy_cache', expire_after=3600)

def get_location(csv_data):
    '''
    receives a list of dictionaries containing addresses in the argument
    returns a list of dictionaries with location (latitude and longitude)
    '''
    geolocator = Nominatim(user_agent="interventions_web_manager")
    geolocator.timeout = 2  # set a timeout for the geocoding service
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    location_data = []
    seen_addresses = {}
    for row in csv_data:
        print(row)
        # Check if latitude and longitude already exist
        if 'latitude' in row and row['latitude'] and 'longitude' in row and row['longitude']:
            location_data.append(row)
            continue

        # Append postal code, city, region, and country to the address
        address = f"{row['Adresse']}, 67000 Strasbourg, Centre, Grand Est, France"
        
        # Check if we already have coordinates for this address
        if address in seen_addresses:
            location = seen_addresses[address]
        else:
            location = geocode(address, addressdetails=True)
            seen_addresses[address] = location

        if location:
            row['latitude'] = location.latitude
            row['longitude'] = location.longitude
        else:
            print(f"Could not geocode address: {address}")
            row['latitude'] = None
            row['longitude'] = None
        
        location_data.append(row)
    
    return location_data
