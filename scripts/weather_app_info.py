import os
import requests

from dotenv import load_dotenv

load_dotenv()

class WeatherAppInfo:
    def __init__(self):
        self.weather_key = os.getenv('OPEN_WEATHER_API_KEY')
        self.cw_url = os.getenv('CURRENT_WEATHER_URL')
        self.hw_url = os.getenv('HOURLY_WEATHER_URL')
        self.latitude = os.getenv('HOME_LAT')
        self.longitude = os.getenv('HOME_LON')

    def get_weather_api_data(self):
        params = {
            'lat':self.latitude,
            'lon':self.longitude,
            'appid':self.weather_key,
            'units':'imperial'
        }
        response = requests.get(self.cw_url,params=params)
        response = response.text
        return response

    def organize_weather_data(self):
        data = self.get_weather_api_data()

        return data



