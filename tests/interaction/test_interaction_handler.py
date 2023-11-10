import unittest
from unittest.mock import MagicMock
from interaction.interaction_handler import InteractionHandler
from services.openai_assistant_service import OpenAIAssistantService
from services.weather_service import WeatherService


class TestInteractionHandler(unittest.TestCase):

    def setUp(self):
        self.openai_service_mock = MagicMock(spec=OpenAIAssistantService)
        self.weather_service_mock = MagicMock(spec=WeatherService)
        self.interaction_handler = InteractionHandler(self.openai_service_mock, self.weather_service_mock)

    def test_handle_user_input(self):
        # Set up the mock responses for weather service
        self.weather_service_mock.get_weather.return_value = {
            'temperature': 70,
            'temperatureUnit': 'F',
            'detailedForecast': 'Clear skies'
        }

        # Mock for openai_service and its functions
        self.openai_service_mock.create_thread.return_value = 'test_thread'
        self.openai_service_mock.create_run.return_value = MagicMock(status="completed")
        self.openai_service_mock.wait_for_run_completion.return_value = MagicMock(status="completed")
        self.openai_service_mock.get_responses.return_value = [
            { 'role': 'assistant', 'content': "The weather is nice." }
        ]

        response = self.interaction_handler.handle_user_input("What's the weather like?")
        self.weather_service_mock.get_weather.assert_called_with("37.7749", "-122.4194")
        self.assertEqual(response, "The weather is nice.")

    # Implement additional test methods here...

if __name__ == '__main__':
    unittest.main()
