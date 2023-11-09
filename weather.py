import requests

WEATHER_BASE_URL = "https://api.weather.gov/points/"

def get_weather(latitude, longitude):
    """
    Get the current weather for a location using the Weather API.

    Args:
    latitude (str): The latitude of the location.
    longitude (str): The longitude of the location.

    Returns:
    dict: A dictionary containing the current weather information.
    """
    url = WEATHER_BASE_URL + latitude + "," + longitude
    headers = {"Accept": "application/geo+json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        forecast_url = data["properties"]["forecast"]
        response = requests.get(forecast_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json()  
    else:
        return response.json()
