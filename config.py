from services.openai_assistant_service import OpenAIAssistantService
from services.weather_service import WeatherService
from utils.service_registry import service_registry

# Config class could also load environment variables, file configurations, etc.
class Config:
    pass

# Instantiate services and register them with the service_registry
openai_assistant_service = OpenAIAssistantService()
weather_service = WeatherService()

service_registry.register_service('OpenAIAssistantService', openai_assistant_service)
service_registry.register_service('WeatherService', weather_service)