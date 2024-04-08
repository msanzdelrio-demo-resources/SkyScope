from flask import render_template, request
from . import app
import requests

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None

    if request.method == 'POST':
        city = request.form['city']

        # Vulnerable code: Directly using user-provided data in URL
        url = 'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=b5268fcd2ca37ab2198170fac2825453'

        response = requests.get(url).json()

        weather = {
            'country': response['sys']['country'],
            'city': response['name'],
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

    return render_template('index.html', weather=weather)

@app.route('/read_file', methods=['POST'])
def read_file():
    # Get the file path from the form data
    file_path = request.form['file_path']

    # Vulnerable code: Directly using user-provided data to open a file
    with open(file_path, 'r') as file:
        content = file.read()

    return content