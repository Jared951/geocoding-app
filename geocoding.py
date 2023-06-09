import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

# Create an instance of the geocoder
# geolocator = Nominatim(user_agent="my_app")



# # List to store geocoded coordinates
# geocoded_data = []

# # Iterate over each address in the list
# for address in addresses:
#     # Use geocoder to geocode the address
#     location = geolocator.geocode(address)
    
#     # Check if geocoding was successful and location object is not None
#     if location is not None:
#         # Retrieve latitude and longitude from the location object
#         latitude = location.latitude # type: ignore
#         longitude = location.longitude # type: ignore
        
#         # Append coordinates to the geocoded_data list
#         geocoded_data.append((latitude, longitude))
#     else:
#         # Print a message if geocoding fails or location is None
#         print(f"Geocoding failed for address: {address}")

# # Save geocoded data to a CSV file
# filename = 'geocoded_coordinates.csv'

# with open(filename, 'w', newline='') as file:
#     # Create a CSV writer object
#     writer = csv.writer(file)
    
#     # Write the geocoded data to the CSV file
#     writer.writerows(geocoded_data)

# # Print a success message
# print(f"Geocoded coordinates saved to {filename}.")






def geocode_address(address):
    geolocator = Nominatim(user_agent="my_app")

    location = geolocator.geocode(address)

    print(location)

    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
    else:
        return False

    return [latitude, longitude]

addresses = [
    "20 W 34th St., New York, NY",
    "400 Broad St, Seattle, WA",
    "1600 Pennsylvania Avenue NW, Washington, DC 20500"
]

print(geocode_address(addresses[0]))





# time out geo code

# def geocode_address(address):
#     geolocator = Nominatim(user_agent="my_app")
#     retries = 3
#     delay = 1  # Delay in seconds between retries
    
#     for _ in range(retries):
#         try:
#             location = geolocator.geocode(address)
#             if location is not None:
#                 latitude = location.latitude
#                 longitude = location.longitude
#                 return [latitude, longitude]
#         except GeocoderTimedOut:
#             # Handle timeout exception
#             time.sleep(delay)
#             continue
    
#     return False
