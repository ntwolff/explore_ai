import requests

WEATHER_BASE_URL = "https://api.weather.gov/points/"

def construct_url(latitude, longitude):
    """
    Construct the URL for the Weather API.

    Args:
    latitude (str): The latitude of the location.
    longitude (str): The longitude of the location.

    Returns:
    str: The constructed URL.
    """
    return f"{WEATHER_BASE_URL}{latitude},{longitude}"

def handle_response(response):
    """
    Handle the response from the Weather API.

    Args:
    response (requests.Response): The response from the Weather API.

    Returns:
    dict: The JSON data from the response, if the request was successful.
    """
    if response.status_code == 200:
        return response.json()
    else:
        return response.json()

def get_weather(latitude, longitude):
    """
    Get the current weather for a location using the Weather API.

    Args:
    latitude (str): The latitude of the location.
    longitude (str): The longitude of the location.

    Returns:
    dict: A dictionary containing the current weather information.
    """
    url = construct_url(latitude, longitude)
    headers = {"Accept": "application/geo+json"}
    response = requests.get(url, headers=headers)
    data = handle_response(response)
    if data:
        forecast_url = data["properties"]["forecast"]
        response = requests.get(forecast_url, headers=headers)
        return handle_response(response)