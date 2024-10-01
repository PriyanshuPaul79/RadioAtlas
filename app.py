import streamlit as st
import requests
import pandas as pd

# Backend API function to get radio stations
def get_radio_stations_by_country(country):
    url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns a list of radio stations
    else:
        return []

# Streamlit frontend logic
st.title('Global Radio Station Player with Map')

# Dropdown to select a country
country = st.selectbox('Select a country', ['United States', 'India', 'Germany', 'France'])

# Fetch radio stations for the selected country
stations = get_radio_stations_by_country(country)

# Display stations and allow the user to select one
if stations:
    station_names = [station['name'] for station in stations]
    selected_station = st.selectbox('Select a station', station_names)

    # Get the selected station data
    selected_station_data = next(station for station in stations if station['name'] == selected_station)
    stream_url = selected_station_data['url_resolved']
    
    # Extract latitude and longitude
    station_lat = selected_station_data.get('latitude')
    station_lon = selected_station_data.get('longitude')

    # Display the audio player
    st.audio(stream_url)

    # Display station info
    st.write(f"Selected Station: {selected_station}")
    st.write(f"Location: Latitude {station_lat}, Longitude {station_lon}")

    # Display the map if location data is available
    if station_lat and station_lon:
        station_location = pd.DataFrame({
            'lat': [station_lat],
            'lon': [station_lon]
        })
        # Display the map using st.map
        st.map(station_location)
    else:
        st.write("No location data available for this station.")

else:
    st.write('No stations found for this country.')
