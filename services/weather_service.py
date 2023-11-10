import requests
from utils.service_registry import service_registry

class WeatherService:
    WEATHER_BASE_URL = "https://api.weather.gov/points/"

    def get_weather(self, latitude, longitude):
        url = f"{self.WEATHER_BASE_URL}{latitude},{longitude}"
        headers = {"Accept": "application/geo+json"}
        response = requests.get(url, headers=headers)
        forecast_url = response.json()["properties"]["forecast"]
        weather_data = requests.get(forecast_url, headers=headers).json()
        
        current_conditions = weather_data["properties"]["periods"][0]
        return {
            'temperature': current_conditions['temperature'],
            'temperatureUnit': current_conditions['temperatureUnit'],
            'detailedForecast': current_conditions['detailedForecast']
        }

# Registering the service with service_registry should happen after instantiation in 'config.py'