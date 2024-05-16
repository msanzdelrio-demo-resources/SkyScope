from flask import render_template, request
from . import app
import requests

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city']

        # Added &units=metric to fetch temperature in Celsius
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b5268fcd2ca37ab2198170fac2825453&units=metric'

        response = requests.get(url).json()

        weather = {
            'country': response['sys']['country'],
            'city': response['name'],
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

    return render_template('index.html', weather=weather)
