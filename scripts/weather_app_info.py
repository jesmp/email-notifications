import os
from dotenv import load_dotenv

load_dotenv()

class WeatherAppInfo:
    def __init__(self):
        self.weather_key = os.getenv('OPEN_WEATHER_API_KEY')

    def get_weather_api_data(self):
        pass

    def organize_weather_data(self):
        pass
