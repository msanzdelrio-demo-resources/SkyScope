from flask import render_template, request
from . import app
import requests
import os

OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_APPID')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city']

        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'

        response = requests.get(url).json()

        weather = {
            'country': response['sys']['country'],
            'city': response['name'],
            'temperature': round(response['main']['temp'] - 273.15, 2),  # Convert Kelvin to Celsius
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
            'wind_speed': response['wind']['speed'],
            'rain': response.get('rain', {}).get('1h', 0),
            'pressure': response['main']['pressure']
        }

    return render_template('index.html', weather=weather)
