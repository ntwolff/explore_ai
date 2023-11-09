import requests
import os
from dotenv import load_dotenv, find_dotenv

BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))

# Your API Key
API_KEY = os.getenv('WEATHER_API_KEY')

# Base URL for the Weather API
WEATHER_BASE_URL = "https://api.weather.gov/points/"

headers = {
    "User-Agent": os.getenv('EMAIL_USER'),
    "Accept": "application/vnd.noaa.dwml+xml;version=1"
}

def get_weather(latitude, longitude):
    """Get the current weather for a location using the Weather API."""
    url = WEATHER_BASE_URL + latitude + "," + longitude
    response = requests.get(url, headers=headers)
    # Check if the response was successful
    if response.status_code == 200:
        data = response.json()
        forecast_url = data["properties"]["forecast"]
        response = requests.get(forecast_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()  # This will contain the error information.
    else:
        return response.json()  # This will contain the error information.
