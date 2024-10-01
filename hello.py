import requests

def get_radio_stations_by_country(country):
    url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns a list of radio stations
    else:
        return []

# Test the function
stations = get_radio_stations_by_country("India")

# Print all stations and check their geo_lat and geo_long
for station in stations[:5]:  # Check only the first 5 stations
    print(f"Station Name: {station['name']}, Latitude: {station['geo_lat']}, Longitude: {station['geo_long']}")

# Now print only those stations that have latitude and longitude
print("\nStations with latitude and longitude:")
for station in stations:
    if station['geo_lat'] is not None and station['geo_long'] is not None:
        print(f"Station Name: {station['name']}, Latitude: {station['geo_lat']}, Longitude: {station['geo_long']}")
