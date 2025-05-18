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
        self.weather_alerts = []

    def get_current_weather_api_data(self):
        params = {
            'lat':self.latitude,
            'lon':self.longitude,
            'units': 'imperial',
            'appid':self.weather_key
        }
        response = requests.get(self.cw_url,params=params)
        return response.json()

    def get_hourly_weather_api_data(self):
        params = {
            'lat':self.latitude,
            'lon':self.longitude,
            'units':'imperial',
            'cnt':4,
            'appid':self.weather_key
        }
        response = requests.get(self.hw_url,params=params)
        return response.json()

    def organize_weather_data(self):
        cw_data = self.get_current_weather_api_data()
        hw_data = self.get_hourly_weather_api_data()

        weather_alert_message = self.check_weather(hw_data)
        full_weather_alert_string = "\n".join(weather_alert_message)

        sunrise_time = self.convert_unix_time(cw_data['sys']['sunrise'])
        sunset_time = self.convert_unix_time(cw_data['sys']['sunset'])

        current_weather = f"Today's weather is {cw_data['weather'][0]['description']}\n"
        current_temperature = f"Temperature is {cw_data['main']['temp']}\u00b0F\n"
        current_feels_like = f"Feels like {cw_data['main']['feels_like']}\u00b0F\n"
        current_humidity = f"Humidity is at {cw_data['main']['humidity']}\n"
        sun_time = f"Sunrise is at {sunrise_time} and Sunset is at {sunset_time}\n"

        full_message = (current_weather + current_temperature + current_feels_like +
                        current_humidity + sun_time + "\n\n" + full_weather_alert_string)

        return full_message

    def convert_unix_time(self,time):
        utc_dt = datetime.fromtimestamp(time,tz=timezone.utc)
        cst = pytz.timezone("America/Chicago")
        cst_time = utc_dt.astimezone(cst)
        formatted_time = cst_time.strftime("%H:%M:%S")
        return formatted_time

    def check_weather(self,hours):
        for hour in hours['list']:
            timestamp = self.convert_unix_time(hour['dt'])
            weather_id = int(hour['weather'][0]['id'])
            if 200 <= weather_id < 600:
                msg_alert = "Pack an umbrella.☂️"
            elif 600 <= weather_id < 700:
                msg_alert = "Stay warm and pack a jacket.🧥"
            elif 700 <= weather_id < 800:
                msg_alert = "Pack for special conditions."
            else:
                msg_alert = "Enjoy the day! Stay Hydrated!🌊"

            message = (f"At {timestamp}, "
                       f"\nForecast: {hour['weather'][0]['main']}:{hour['weather'][0]['description']}, "
                       f"\nTemperature:{hour['main']['temp']}\u00b0F"
                       f"\nFeels Like:{hour['main']['feels_like']}\u00b0F"
                       f"\nHumidity:{hour['main']['humidity']}"
                       f"\nMessage Alert:{msg_alert}\n")
            self.weather_alerts.append(message)

        return self.weather_alerts