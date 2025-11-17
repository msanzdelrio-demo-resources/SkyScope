from flask import render_template, request
from . import app
import requests
import os
import re

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_APPID')

def get_mock_weather_data(city):
    """Return mock weather data for testing purposes."""
    return {
        'country': 'XX',
        'city': city,
        'temperature': 15.5,
        'description': 'clear sky',
        'icon': '01d',
        'wind_speed': 5.2,
        'rain': 0,
        'pressure': 1013
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city']

        # Validate city name to prevent partial SSRF and injection attacks
        if not re.match(r"^[a-zA-Z\s\-']{1,64}$", city):
            weather = None  # or optionally: weather = {'error': 'Invalid city name.'}
        # Use mock data when in testing mode
        elif app.testing:
            weather = get_mock_weather_data(city)
        else:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'
            response = requests.get(url).json()
            weather = {
                'country': response['sys']['country'],
                'city': response['name'],
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'wind_speed': response['wind']['speed'],
                'rain': response.get('rain', {}).get('1h', 0),
                'pressure': response['main']['pressure']
            }

    return render_template('index.html', weather=weather)
