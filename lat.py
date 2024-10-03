import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os
from streamlit import session_state as state

# Function to get radio stations by country with caching
@st.cache_data
def get_radio_stations_by_country(country):
    url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return []

# Function to get unique values for genres, languages, etc.
def get_unique_values(stations, key):
    return sorted(set([station[key] for station in stations if station.get(key)]))

# Mapping of countries to local flag file paths
country_flags = {
    'India': 'assets/globe_India.jpg',
    'Canada': 'assets/globe_canada.jpg',
    'Brazil': 'assets/globe_brazil.jpg',
    'United Kingdom': 'assets/globe_uk.jpg',
    'Germany': 'assets/globe_germany.jpg'
}

# Streamlit app starts here
st.title('🎧 RadioAtlas')

# Initialize favorites in session state
if 'favorites' not in state:
    state['favorites'] = []

# Select a country
countries = list(country_flags.keys())
selected_country = st.selectbox('🌍 Select a Country', countries)

# Display the flag of the selected country
if selected_country in country_flags:
    flag_path = country_flags[selected_country]
    if os.path.exists(flag_path):
        st.image(flag_path, use_column_width=True)
    else:
        st.error("Flag image not found.")

# Fetch and display radio stations for the selected country
stations = get_radio_stations_by_country(selected_country)

if stations:
    # Search bar to filter radio stations
    search_query = st.text_input('🔍 Search for a Station', '')

    # Filters for genre, language, and bitrate
    genres = get_unique_values(stations, 'tags')
    languages = get_unique_values(stations, 'language')
    bitrates = sorted(set([station['bitrate'] for station in stations if station.get('bitrate')]))

    selected_genre = st.selectbox('🎶 Filter by Genre', ['All'] + genres)
    selected_language = st.selectbox('🗣️ Filter by Language', ['All'] + languages)
    selected_bitrate = st.selectbox('📶 Filter by Bitrate', ['All'] + [str(b) for b in bitrates])

    # Filter stations based on search and filter inputs
    filtered_stations = [station for station in stations
                         if (search_query.lower() in station['name'].lower())
                         and (selected_genre == 'All' or selected_genre in station['tags'])
                         and (selected_language == 'All' or station['language'] == selected_language)
                         and (selected_bitrate == 'All' or station['bitrate'] == int(selected_bitrate))]

    st.write(f"Found {len(filtered_stations)} stations matching your criteria.")

    if filtered_stations:
        station_names = [station['name'] for station in filtered_stations]
        selected_station = st.selectbox('📻 Select a Station', station_names)

        # Get selected station's data
        selected_station_data = next(station for station in filtered_stations if station['name'] == selected_station)
        stream_url = selected_station_data['url_resolved']
        station_lat = selected_station_data.get('geo_lat')
        station_lon = selected_station_data.get('geo_long')
        station_lang = selected_station_data.get('language')
        station_bitrate = selected_station_data.get('bitrate')

        # Display the audio player
        st.audio(stream_url)
        st.write(f"🎶 Language: {station_lang or 'Not Available'}")
        st.write(f"📶 Bitrate: {station_bitrate or 'Not Available'} kbps")

        # Add to favorites button
        if st.button(f'❤️ Add {selected_station} to Favorites'):
            if selected_station not in state['favorites']:
                state['favorites'].append(selected_station)
                st.success(f'Added {selected_station} to Favorites!')
            else:
                st.warning(f'{selected_station} is already in your favorites.')

        # Display favorite stations
        if state['favorites']:
            st.subheader('Your Favorite Stations:')
            for favorite_station in state['favorites']:
                st.write(f"- {favorite_station}")

        # Show station location on map
        if station_lat and station_lon:
            st.write(f"📍 Station Location: Latitude {station_lat}, Longitude {station_lon}")

            # Create map centered on the radio station's location
            station_map = folium.Map(location=[station_lat, station_lon], zoom_start=12)

            # Add marker for the radio station
            folium.Marker([station_lat, station_lon], popup=f"{selected_station}").add_to(station_map)

            # Display map with station location
            st_folium(station_map, width=700, height=500)
        else:
            st.warning("Location data not available for this station.")
    else:
        st.warning("No stations found for your search or filters.")
else:
    st.error(f'No stations found for {selected_country}.')

