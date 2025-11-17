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
            'country': response.get('sys', {}).get('country', 'Unknown'),
            'city': response.get('name', 'Unknown'),
            'temperature': response.get('main', {}).get('temp', 0),
            'description': response.get('weather', [{}])[0].get('description', 'N/A'),
            'icon': response.get('weather', [{}])[0].get('icon', ''),
            'wind_speed': response.get('wind', {}).get('speed', 0),
            'rain': response.get('rain', {}).get('1h', 0),
            'pressure': response.get('main', {}).get('pressure', 0)
        }

    return render_template('index.html', weather=weather)
