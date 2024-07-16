from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import requests_cache

requests_cache.install_cache('geopy_cache', expire_after=3600)

def get_location(csv_data):
    '''
    receives a dict of addresses in the argument
    returns a dict of location (latitude and longitude)
    '''
    geolocator = Nominatim(user_agent="interventions_web_manager")
    geolocator.timeout = 2  # set a timeout for the geocoding service
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    
    location_data = []
    seen_addresses = {}
    address_found = 0
    duplicate_address = 0
    for row in csv_data:
        # Append postal code, city, region, and country to the address
        address = f"{row['Adresse']}, 67000 strasbourg, centre, Grand Est, France"
        
        # Check if we already have coordinates for this address
        if address in seen_addresses:
            location = seen_addresses[address]
            duplicate_address = duplicate_address + 1
            print(f'{duplicate_address} duplicates')
        else:
            location = geocode(address, addressdetails=True)
            address_found = address_found + 1
            print(address_found)
            print(location)
            seen_addresses[address] = location

        if location:
            row['latitude'] = location.latitude
            row['longitude'] = location.longitude
            location_data.append(row)
        else:
            print(f"Could not geocode address: {address}")
    
    return location_data
