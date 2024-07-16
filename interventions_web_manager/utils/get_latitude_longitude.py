from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests_cache
import time

# Set up caching to avoid hitting the rate limit
requests_cache.install_cache('geocode_cache', expire_after=3600)

def get_location(csv_data, retries=3):
    '''
    Receives a list of addresses in the argument
    Returns a list of dicts with location (latitude and longitude)
    '''
    geolocator = Nominatim(user_agent="interventions_web_manager")
    locations = []
    address_cache = {}

    def geocode_address(address, retries):
        if address in address_cache:
            #this helps us by checking for duplicates thus saving time
            return address_cache[address]

        for attempt in range(retries):
            try:
                location = geolocator.geocode(address)
                address_cache[address] = location
                return location
            # geocoder has batch limit so we need to avoid getting timedout
            except GeocoderTimedOut:
                if attempt < retries - 1:
                    time.sleep(1)
                else:
                    return None

    for row in csv_data:
        # modify the dict to gather the latitude and longitude
        # this data will help us in the frontend with Leaflet.js to map out the interventions
        address = row['Adresse']
        location = geocode_address(address, retries)
        if location:
            row['latitude'] = location.latitude
            row['longitude'] = location.longitude
        else:
            row['latitude'] = None
            row['longitude'] = None
        locations.append(row)

    return locations