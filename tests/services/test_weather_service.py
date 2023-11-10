import unittest
from unittest.mock import patch
from services.weather_service import WeatherService


class TestWeatherService(unittest.TestCase):

    @patch('services.weather_service.requests.get')
    def test_get_weather(self, mock_get):
        service = WeatherService()
        mock_response = {
            "properties": {
                "forecast": "fake_forecast_url"
            }
        }
        forecast_data = {
            "properties": {
                "periods": [{
                    'temperature': 70,
                    'temperatureUnit': 'F',
                    'detailedForecast': 'Clear skies'
                }]
            }
        }

        # Mock responses for URLs
        mock_get.side_effect = [
            unittest.mock.Mock(**{"json.return_value": mock_response}),
            unittest.mock.Mock(**{"json.return_value": forecast_data})
        ]

        latitude = '37.7749'
        longitude = '-122.4194'
        weather = service.get_weather(latitude, longitude)

        self.assertEqual(weather['temperature'], 70)
        self.assertEqual(weather['temperatureUnit'], 'F')
        self.assertEqual(weather['detailedForecast'], 'Clear skies')

if __name__ == '__main__':
    unittest.main()