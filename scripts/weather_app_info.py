from datetime import datetime, timezone
from zoneinfo import ZoneInfo

import os
import requests
import pytz

from dotenv import load_dotenv

load_dotenv()

class WeatherAppInfo:
    def __init__(self):
        self.weather_key = os.getenv('OPEN_WEATHER_API_KEY')
        self.cw_url = os.getenv('CURRENT_WEATHER_URL')
        self.hw_url = os.getenv('HOURLY_WEATHER_URL')
        self.latitude = os.getenv('HOME_LAT')
        self.longitude = os.getenv('HOME_LON')

    def get_current_weather_api_data(self):
        params = {
            'lat':self.latitude,
            'lon':self.longitude,
            'appid':self.weather_key,
            'units':'imperial'
        }
        response = requests.get(self.cw_url,params=params)
        return response.json()

    def get_hourly_weather_api_data(self):
        params = {
            'lat':self.latitude,
            'lon':self.longitude,
            'appid':self.weather_key
        }
        response = requests.get(self.hw_url,params=params)
        return response.json()

    def organize_weather_data(self):
        cw_data = self.get_current_weather_api_data()
        hw_data =
        sunrise_time = self.convert_unix_time(cw_data['sys']['sunrise'])
        sunset_time = self.convert_unix_time(cw_data['sys']['sunset'])

        current_weather = f"Today's weather is {cw_data['weather'][0]['description']}\n"
        current_temperature = f"Temperature is {cw_data['main']['temp']}\u00b0F\n"
        current_feels_like = f"Feels like {cw_data['main']['feels_like']}\u00b0F\n"
        current_humidity = f"Humidity is at {cw_data['main']['humidity']}\n"
        sun_time = f"Sunrise is at {sunrise_time} and Sunset is at {sunset_time}\n"

        full_message = (current_weather + current_temperature + current_feels_like +
                        current_humidity + sun_time)

        return full_message

    def convert_unix_time(self,time):
        utc_dt = datetime.fromtimestamp(time,tz=timezone.utc)
        cst = pytz.timezone("America/Chicago")
        cst_time = utc_dt.astimezone(cst)
        formatted_time = cst_time.strftime("%H:%M:%S")
        return formatted_time