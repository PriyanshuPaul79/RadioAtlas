import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os
import json
import random
from streamlit import session_state as state

### NEW: Create a cache directory on startup ###
# This ensures there's a place to store the offline station data.
if not os.path.exists('cache'):
    os.makedirs('cache')

### MODIFIED: Function to get radio stations with offline caching ###
# Removed @st.cache_data decorator to fix CacheReplayClosureError
def get_radio_stations_by_country(country, force_refresh=False):
    """
    Fetches radio stations from the API.
    1. Tries to get live data from the API.
    2. If successful, saves the data to a local cache file.
    3. If the API fails, it tries to load data from the cache file.
    4. If both fail, it returns an empty list.

    Args:
        country (str): The country to fetch radio stations for
        force_refresh (bool, optional): If True, bypasses the cache and forces a new API request. Defaults to False.
    """
    # Since we removed the cache decorator, we don't need to clear the cache
    # The force_refresh parameter will still be used to bypass the local file cache
    cache_file = f"cache/{country.lower().replace(' ', '_')}_stations.json"
    url = f"https://de1.api.radio-browser.info/json/stations/bycountry/{country}"

    # If force_refresh is True or if the cache file doesn't exist, always try to fetch from API first
    if force_refresh or not os.path.exists(cache_file):
        try:
            # Step 1: Try to fetch live data
            response = requests.get(url, timeout=10)  # Added a timeout for safety
            response.raise_for_status()
            stations = response.json()

            # Step 2: If successful, save to the cache file
            with open(cache_file, 'w') as f:
                json.dump(stations, f)

            # Let the user know we got live data
            if 'loaded_from_cache' not in state or not state.loaded_from_cache:
                st.toast("✅ Fetched live station data!")
            state.loaded_from_cache = False
            return stations
        except requests.exceptions.RequestException as e:
            if not os.path.exists(cache_file):
                # If no cache exists and API fails
                st.error(f"No cached data is available for {country}. The app cannot run without an initial network connection.")
                return []
            # If API fails but cache exists, continue to the cache loading code below
            st.warning(f"Could not fetch live data. Attempting to load from local cache.")

    # If not force_refresh or if API fetch failed but cache exists, try to load from cache
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r') as f:
                stations = json.load(f)
                st.info(f"Displaying cached data for {country}. Some stations may be outdated.")
                state.loaded_from_cache = True
                return stations
        except (json.JSONDecodeError, IOError):
            st.error("Failed to read the cache file. It might be corrupted.")
            return []
    else:
        # Step 4: If API fails and no cache exists
        st.error(f"No cached data is available for {country}. The app cannot run without an initial network connection.")
        return []

# Function to get unique values for genres, languages, etc.
def get_unique_values(stations, key):
    # Handles cases where the key might be missing or the value is a list (like 'tags')
    values = set()
    for station in stations:
        if station.get(key):
            # Tags can be a single string with commas
            if key == 'tags' and isinstance(station[key], str):
                values.update([tag.strip() for tag in station[key].split(',') if tag.strip()])
            else:
                values.add(station[key])
    return sorted(list(values))

# Mapping of countries to local flag file paths
# Updated with new consistent style images
country_flags = {
    'India': 'assets/globe_India.jpg',
    'Canada': 'assets/globe_canada.png',
    'Brazil': 'assets/globe_brazil.jpg',
    'United Kingdom': 'assets/globe_uk.png',
    'Germany': 'assets/globe_germany.png'
}

# Streamlit app starts here
st.title('📻 RadioAtlas')

# Initialize favorites in session state
if 'favorites' not in state:
    state['favorites'] = []

# Select a country
countries = list(country_flags.keys())
col1, col2 = st.columns([3, 1])
selected_country = col1.selectbox('🌍 Select a Country', countries)

# Add refresh button
refresh_data = col2.button('🔄 Refresh Data')
if refresh_data:
    st.toast("Refreshing station data from API...")
    # We'll pass force_refresh=True when calling get_radio_stations_by_country

# Display the flag of the selected country
if selected_country in country_flags:
    flag_path = country_flags[selected_country]
    if os.path.exists(flag_path):
        st.image(flag_path, use_column_width=True)
    else:
        st.warning("New image file not found. Please follow the instructions in IMAGE_REPLACEMENT_INSTRUCTIONS.md to update the country images.")
        # Try to fall back to the old image naming convention
        old_flag_path = flag_path.replace('map_', 'globe_')
        if os.path.exists(old_flag_path):
            st.image(old_flag_path, use_column_width=True)
            st.info("Using legacy image. For a better experience, please update to the new image style.")
        else:
            st.error("No image found for this country.")

# Fetch and display radio stations for the selected country
stations = get_radio_stations_by_country(selected_country, force_refresh=refresh_data)

if stations:
    # Search bar to filter radio stations
    search_query = st.text_input('🔎 Search for a Station', '')

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
                         and (selected_bitrate == 'All' or str(station.get('bitrate', '')) == selected_bitrate)]

    st.write(f"Found {len(filtered_stations)} stations matching your criteria.")

    if filtered_stations:
        station_names = [station['name'] for station in filtered_stations]
        selected_station_name = st.selectbox('📡 Select a Station', station_names)

        # Get selected station's data
        selected_station_data = next((station for station in filtered_stations if station['name'] == selected_station_name), None)

        if selected_station_data:
            stream_url = selected_station_data['url_resolved']
            station_lat = selected_station_data.get('geo_lat')
            station_lon = selected_station_data.get('geo_long')
            station_lang = selected_station_data.get('language')
            station_bitrate = selected_station_data.get('bitrate')

            # Display the audio player
            st.audio(stream_url)
            st.write(f"**Language:** {station_lang or 'Not Available'} | **Bitrate:** {station_bitrate or 'Not Available'} kbps")

            # Add to favorites button
            if st.button(f'❤️ Add {selected_station_name} to Favorites'):
                if selected_station_name not in state['favorites']:
                    state['favorites'].append(selected_station_name)
                    st.success(f'Added {selected_station_name} to Favorites!')
                else:
                    st.warning(f'{selected_station_name} is already in your favorites.')

            ### NEW: Feature 3 - "You Might Also Like..." ###
            st.subheader("You Might Also Like...")
            selected_tags = set(tag.strip() for tag in selected_station_data.get('tags', '').split(',') if tag.strip())

            if selected_tags:
                recommendations = []
                for station in stations:
                    if station['name'] == selected_station_name:
                        continue  # Skip the currently selected station

                    station_tags = set(tag.strip() for tag in station.get('tags', '').split(',') if tag.strip())

                    if selected_tags.intersection(station_tags):
                        recommendations.append(station['name'])

                    if len(recommendations) >= 5:  # Limit to 5 recommendations
                        break

                if recommendations:
                    for rec_name in recommendations:
                        # Find the full station data for this recommendation
                        rec_station = next((s for s in stations if s['name'] == rec_name), None)
                        if rec_station:
                            # Format tags for better readability
                            tags = rec_station.get('tags', '')
                            formatted_tags = ', '.join([tag.strip() for tag in tags.split(',') if tag.strip()]) if tags else 'N/A'
                            # Display station with additional info
                            st.write(f"• **{rec_name}** - Language: {rec_station.get('language', 'N/A')}, Genre: {formatted_tags}")
                        else:
                            st.write(f"• {rec_name}")
                else:
                    st.info("No similar stations found based on genre.")
            else:
                st.info("This station has no genre tags to find similar ones.")

        # Display favorite stations
        if state['favorites']:
            st.subheader('⭐ Your Favorite Stations:')
            for favorite_station in state['favorites']:
                st.write(f"• {favorite_station}")

        ### NEW: Feature 2 - "Radio Roulette" ###
        st.subheader("Discovery Zone")
        if st.button("🎲 Radio Roulette"):
            roulette_pick = None
            # Prefer stations with similar genre/language to favorites
            if state['favorites']:
                fav_stations_data = [s for s in stations if s['name'] in state['favorites']]
                fav_tags = set()
                fav_langs = set()
                for s in fav_stations_data:
                    fav_tags.update(t.strip() for t in s.get('tags', '').split(',') if t.strip())
                    if s.get('language'):
                        fav_langs.add(s.get('language'))

                potential_picks = [
                    s for s in stations 
                    if (fav_tags and set(tag.strip() for tag in s.get('tags', '').split(',') if tag.strip()).intersection(fav_tags)) or \
                       (fav_langs and s.get('language') in fav_langs)
                ]
                if potential_picks:
                    roulette_pick = random.choice(potential_picks)

            # Fallback to any random station if no favorites or no matches found
            if not roulette_pick and stations:
                roulette_pick = random.choice(stations)

            if roulette_pick:
                st.success(f"You got: **{roulette_pick['name']}**!")
                st.audio(roulette_pick['url_resolved'])
                # Format tags for better readability
                tags = roulette_pick.get('tags', '')
                formatted_tags = ', '.join([tag.strip() for tag in tags.split(',') if tag.strip()]) if tags else 'N/A'
                st.write(f"**Language:** {roulette_pick.get('language', 'N/A')} | **Genre:** {formatted_tags}")

        # Show station location on map
        if selected_station_data and station_lat and station_lon:
            st.write(f"📍 Station Location: Latitude {station_lat}, Longitude {station_lon}")
            station_map = folium.Map(location=[station_lat, station_lon], zoom_start=12)
            folium.Marker([station_lat, station_lon], popup=f"{selected_station_name}").add_to(station_map)
            st_folium(station_map, width=700, height=500)
        else:
            st.warning("Location data not available for this station.")
    else:
        st.warning("No stations found for your search or filters.")
else:
    st.error(f'Could not load any station data for {selected_country}.')