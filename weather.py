import requests
from configparser import ConfigParser

class OpenWeatherMap:
    def __init__(self, unit=1):
        self.weather_des = ''
        self.weather_icon = ''
        self.temperature = None

        try:
            self.API_KEY = self._get_api_key()
        except Exception as e:
            print(f"Error occured while getting api key: {e}")

        self.CITY_NAME = ''
        self.UNIT_TPYE = ['imperial', 'metric', 'standard'][unit]
        self.UNITS = {'imperial' : '°F', 'metric': '°C', 'standard': '°K'}
        self.PARAMS = {'q': self.CITY_NAME,
                       'appid': self.API_KEY, 'units': self.UNIT_TPYE}
        self.url = f'https://api.openweathermap.org/data/2.5/weather'
        self.error = False
        self.weather_icons = {
            '01d': '☀️',
            '01n': '🌙',
            '02d': '⛅',
            '02n': '⛅',
            '03d': '☁️',
            '03n': '☁️',
            '04d': '☁️',
            '04n': '☁️',
            '09d': '🌧️',     
            '09n': '🌧️',
            '10d': '🌦️',        
            '10n': '🌦️',
            '11d': '⛈️',
            '11n': '⛈️',
            '13d': '❄️',     
            '13n': '❄️', 
            '50d': '🌫️',            
            '50n': '🌫️'
        }


    def _get_api_key(self):
        config = ConfigParser()
        config.read('secrets.ini')
        return config['openweather']['api_key']


    def get_icon(self, icon_id):
        return self.weather_icons[icon_id]


    def get_weather(self, city):
        self.CITY_NAME = city
        self.PARAMS['q'] = self.CITY_NAME
        try:
            response = requests.get(self.url, params=self.PARAMS)
            data = response.json()
            
            if data['cod'] == '404':
                self.error = True
                raise Exception("City not found")

            else:    
                weather = data['weather'][0]
                self.weather_des = weather['description']
                self.weather_icon = self.get_icon(weather['icon'])

                main = data['main']
                self.temperature = f"{main['temp']} {self.UNITS[self.UNIT_TPYE]}"

        except Exception as e:
            print(f"Error occured while getting weather data. \nError: {e}")
