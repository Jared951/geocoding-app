import csv
from geopy.geocoders import Nominatim

# Create an instance of the geocoder
geolocator = Nominatim(user_agent="my_app")

# List of addresses to geocode
addresses = [
    "20 W 34th St., New York, NY",
    "400 Broad St, Seattle, WA",
    "1600 Pennsylvania Avenue NW, Washington, DC 20500"
]

# List to store geocoded coordinates
geocoded_data = []

# Iterate over each address in the list
for address in addresses:
    # Use geocoder to geocode the address
    location = geolocator.geocode(address)
    
    # Check if geocoding was successful and location object is not None
    if location is not None:
        # Retrieve latitude and longitude from the location object
        latitude = location.latitude
        longitude = location.longitude
        
        # Append coordinates to the geocoded_data list
        geocoded_data.append((latitude, longitude))
    else:
        # Print a message if geocoding fails or location is None
        print(f"Geocoding failed for address: {address}")

# Save geocoded data to a CSV file
filename = 'geocoded_coordinates.csv'

with open(filename, 'w', newline='') as file:
    # Create a CSV writer object
    writer = csv.writer(file)
    
    # Write the geocoded data to the CSV file
    writer.writerows(geocoded_data)

# Print a success message
print(f"Geocoded coordinates saved to {filename}.")