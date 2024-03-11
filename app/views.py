from flask import render_template, request  # Import necessary modules from Flask
from . import app  # Import the Flask app object from the current package
import requests  # Import the requests module for making HTTP requests

@app.route('/', methods=['GET', 'POST'])  # Define a route for the root URL ("/") that responds to both GET and POST requests
def index():  # Define the function to handle requests to the root URL
    weather = None  # Initialize a variable to hold the weather data

    if request.method == 'POST':  # If the request method is POST
        city = request.form['city']  # Extract the city name from the form data

        # Construct the URL for the OpenWeatherMap API
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=b5268fcd2ca37ab2198170fac2825453'

        response = requests.get(url).json()  # Send a GET request to the URL and parse the JSON response into a Python dictionary

        # Populate the weather dictionary with data from the response
        weather = {
            'country': response['sys']['country'],  # Country
            'city': response['name'],  # City name
            'temperature': round(response['main']['temp'] - 273.15, 1),  # Temperature in Celsius, rounded to 1 decimal place
            'description': response['weather'][0]['description'],  # Weather description
            'icon': response['weather'][0]['icon'],  # Weather icon
        }

    # Render the 'index.html' template and pass the weather data to it
    return render_template('index.html', weather=weather)
