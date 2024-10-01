# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import requests

# # Function to get radio stations by country
# def get_radio_stations_by_country(country):
#     url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()  # Returns a list of radio stations
#     else:
#         return []

# # Streamlit app starts here
# st.title('RadioAtlas')

# # Select a country
# countries = ['India', 'Canada', 'Brazil', 'UK', 'Germany']  # List of countries
# selected_country = st.selectbox('Select a Country', countries)

# # Fetch and display radio stations for the selected country
# if selected_country:
#     stations = get_radio_stations_by_country(selected_country)

#     if stations:
#         station_names = [station['name'] for station in stations]
#         selected_station = st.selectbox('Select a Station', station_names)

#         # Get the selected station's data including latitude and longitude
#         selected_station_data = next(station for station in stations if station['name'] == selected_station)
#         stream_url = selected_station_data['url_resolved']
#         station_lat = selected_station_data.get('geo_lat')
#         station_lon = selected_station_data.get('geo_long')
#         station_lang= selected_station_data.get('language')
#         # Display the audio player
#         st.audio(stream_url)
#         if station_lang is not None:
#             st.write(f"Langage used is {station_lang}")
#         else: 
#             st.write("")

#         # Show the station's location on the map
#         if station_lat is not None and station_lon is not None:
#             st.write(f"Radio Station Location: Latitude {station_lat}, Longitude {station_lon}")

#             # Create a map centered on the radio station's location
#             station_map = folium.Map(location=[station_lat, station_lon], zoom_start=12)

#             # Add a marker for the radio station
#             folium.Marker([station_lat, station_lon], popup=f"{selected_station}").add_to(station_map)

#             # Display the updated map with the station location
#             st_folium(station_map, width=700, height=500)
#         else:
#             st.write("No location data available for this station.")
#     else:
#         st.write(f'No stations found for {selected_country}.')

# import streamlit as st
# import folium
# from streamlit_folium import st_folium
# import requests
# import os

# # Function to get radio stations by country
# def get_radio_stations_by_country(country):
#     url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"
#     response = requests.get(url)
#     if response.status_code == 200:
#         return response.json()  # Returns a list of radio stations
#     else:
#         return []

# # Mapping of countries to local flag file paths
# country_flags = {
#     'India': 'assets/India.jpg',
#     'Canada': 'assets/canada.jpg',
#     'Brazil': 'assets/Brazil.jpg',
#     'UK': 'flags/flag_of_uk.png',
#     'Germany': 'flags/flag_of_germany.png'
# }

# # Streamlit app starts here
# st.title('RadioAtlas')

# # Select a country
# countries = list(country_flags.keys())  # List of countries from the dictionary
# selected_country = st.selectbox('Select a Country', countries)

# # Display the flag of the selected country
# if selected_country in country_flags:
#     flag_path = country_flags[selected_country]
#     if os.path.exists(flag_path):  # Check if the file exists
#         st.image(flag_path, use_column_width=True)
#     else:
#         st.write("Flag image not found.")

# # Fetch and display radio stations for the selected country
# if selected_country:
#     stations = get_radio_stations_by_country(selected_country)

#     if stations:
#         station_names = [station['name'] for station in stations]
#         selected_station = st.selectbox('Select a Station', station_names)

#         # Get the selected station's data including latitude and longitude
#         selected_station_data = next(station for station in stations if station['name'] == selected_station)
#         stream_url = selected_station_data['url_resolved']
#         station_lat = selected_station_data.get('geo_lat')
#         station_lon = selected_station_data.get('geo_long')
#         station_lang = selected_station_data.get('language')

#         # Display the audio player
#         st.audio(stream_url)
#         if station_lang is not None:
#             st.write(f"Language used is {station_lang}")
#         else: 
#             st.write("")

#         # Show the station's location on the map
#         if station_lat is not None and station_lon is not None:
#             st.write(f"Radio Station Location: Latitude {station_lat}, Longitude {station_lon}")

#             # Create a map centered on the radio station's location
#             station_map = folium.Map(location=[station_lat, station_lon], zoom_start=12)

#             # Add a marker for the radio station
#             folium.Marker([station_lat, station_lon], popup=f"{selected_station}").add_to(station_map)

#             # Display the updated map with the station location
#             st_folium(station_map, width=700, height=500)
#         else:
#             st.write("No location data available for this station.")
#     else:
#         st.write(f'No stations found for {selected_country}.')




import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os

# Function to get radio stations by country
def get_radio_stations_by_country(country):
    url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns a list of radio stations
    else:
        return []

# Mapping of countries to local flag file paths
country_flags = {
    'India': 'assets/India.jpg',
    'Canada': 'assets/canada.jpg',
    'Brazil': 'assets/Brazil.jpg',
    'UK': 'flags/flag_of_uk.png',
    'Germany': 'flags/flag_of_germany.png'
}

# Streamlit app starts here
st.title('RadioAtlas')

# Select a country
countries = list(country_flags.keys())  # List of countries from the dictionary
selected_country = st.selectbox('Select a Country', countries)

# Display the flag of the selected country
if selected_country in country_flags:
    flag_path = country_flags[selected_country]
    if os.path.exists(flag_path):  # Check if the file exists
        st.image(flag_path, use_column_width=True)
    else:
        st.write("Flag image not found.")

# Fetch and display radio stations for the selected country
if selected_country:
    stations = get_radio_stations_by_country(selected_country)

    if stations:
        # Search bar to filter radio stations
        search_query = st.text_input('Search for a Station', '')

        # Filter stations by search query
        if search_query:
            station_names = [station['name'] for station in stations if search_query.lower() in station['name'].lower()]
        else:
            station_names = [station['name'] for station in stations]

        if station_names:
            selected_station = st.selectbox('Select a Station', station_names)

            # Get the selected station's data including latitude and longitude
            selected_station_data = next(station for station in stations if station['name'] == selected_station)
            stream_url = selected_station_data['url_resolved']
            station_lat = selected_station_data.get('geo_lat')
            station_lon = selected_station_data.get('geo_long')
            station_lang = selected_station_data.get('language')

            # Display the audio player
            st.audio(stream_url)
            if station_lang is not None:
                st.write(f"Language used is {station_lang}")
            else: 
                st.write("")

            # Show the station's location on the map
            if station_lat is not None and station_lon is not None:
                st.write(f"Radio Station Location: Latitude {station_lat}, Longitude {station_lon}")

                # Create a map centered on the radio station's location
                station_map = folium.Map(location=[station_lat, station_lon], zoom_start=12)

                # Add a marker for the radio station
                folium.Marker([station_lat, station_lon], popup=f"{selected_station}").add_to(station_map)

                # Display the updated map with the station location
                st_folium(station_map, width=700, height=500)
            else:
                st.write("No location data available for this station.")
        else:
            st.write("No stations found for your search.")
    else:
        st.write(f'No stations found for {selected_country}.')
