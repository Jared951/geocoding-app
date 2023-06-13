import csv
import geopy
from geopy.geocoders import Nominatim
from model import db, Address
from geopy.exc import GeocoderTimedOut
import time

geolocator = Nominatim(user_agent="my_app")

def geocode_address(address_name, max_retries=3, retry_delay=1):
    geolocator = Nominatim(user_agent="my_app")

    retries = 0
    while retries < max_retries:
        try:
            location = geolocator.geocode(address_name)

            if location is not None:
                latitude = location.latitude
                longitude = location.longitude 

                # Update the address in the database with the geocoordinates
                address = Address.query.filter_by(address_name=address_name).first()
                address.latitude = latitude
                address.longitude = longitude
                db.session.commit()

                return [latitude, longitude]
            else:
                return False

        except geopy.exc.GeocoderTimedOut:
            # Service timeout occurred, retry after delay
            retries += 1
            time.sleep(retry_delay)

    return False  # Geocoding failed after maximum retries