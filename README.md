# 🎧 RadioAtlas

**RadioAtlas** is a Streamlit-based web application that allows users to explore and listen to radio stations from various countries. The app provides an intuitive interface to filter stations by genre, language, bitrate, and also includes a feature to save favorite stations. Additionally, it visualizes the geographical location of the stations on a map using `folium`.

## Features
- 🌍 **Country Selection**: Choose from a list of countries and explore radio stations from that region.
- 🔍 **Search & Filter**: Search for radio stations and filter them by genre, language, or bitrate.
- 📻 **Listen to Stations**: Play the selected radio stations directly within the app.
- ❤️ **Favorites**: Add stations to your favorites for easy access later.
- 📍 **Map Integration**: View the geographical location of radio stations on an interactive `folium` map.
- 🎨 **Flag Display**: See the country flag corresponding to the selected country.
- 💾 **Offline Caching**: Works offline after first load by caching station data.
- 🎲 **Radio Roulette**: Discover a random station, with a preference for your favorite genres/languages.
- 🤝 **Recommendations**: Get "You Might Also Like..." suggestions based on the selected station's genre.

## Screenshots

> _Below are some screenshots of the app in action:_

### Home Page
![Home Page](screenshots/screenshot_home.png)

### Filters and Station List
![Filters and Station List](screenshots/screenshot_filters.png)

### Station Map View
![Station Map](screenshots/screenshot_map.png)

### Favorites and Recommendations
![Favorites and Recommendations](screenshots/screenshot_favorites.png)

*You can add or update screenshots in the `screenshots/` folder.*

## Installation

To run the application locally, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/RadioAtlas.git
   cd RadioAtlas
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:

   ```bash
   streamlit run radioatlas_updated.py
   ```

## Dependencies

- [Streamlit](https://streamlit.io/) for the UI and frontend.
- [Folium](https://python-visualization.github.io/folium/) for displaying maps.
- [Streamlit-Folium](https://github.com/randyzwitch/streamlit-folium) to integrate Folium maps into Streamlit.
- [Requests](https://docs.python-requests.org/en/latest/) to fetch radio station data from the Radio Browser API.

You can install all dependencies using the provided `requirements.txt` file.

## Usage

1. Select a country from the dropdown list.
2. Search or filter radio stations by genre, language, or bitrate.
3. Choose a station from the filtered results and start listening!
4. View the station's location on a map and add it to your favorites for future listening.

## Country Flags

Local flag images are stored in the `assets` folder. Make sure the correct path for the flag files is provided, or the app will display an error.

## API

This app uses the [Radio Browser API](https://de1.api.radio-browser.info/) to fetch radio station data by country.

## Contributing

Feel free to submit issues or contribute to the project by creating a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
