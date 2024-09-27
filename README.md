# My Weather App

This is a simple weather application built with Flask. It allows users to enter a city name and get the current weather information for that city.

# Installation

1. Clone the repository:
```sh
git clone https://github.com/yourusername/my-weather-app.git
```
2. Navigate to the project directory:
```sh
cd my-weather-app
```
3. Install the required Python packages:
```sh
pip install -r requirements.txt
```

# Usage

To run the application, execute the following command in the project directory:
python run.py
Then, open your web browser and navigate to http://localhost:5000.

# Files

- app/views.py: Contains the Flask routes and the main logic of the application.
- app/templates/index.html: The HTML template for the main page.
- app/static/css/main.css: The CSS styles for the application.
- app/static/js/main.js: The JavaScript code for handling form submission.
- tests/test_views.py: Contains unit tests for the application.

Testing

To run the tests, execute the following command in the project directory:
python -m unittest discover tests

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License

MIT (https://choosealicense.com/licenses/mit/)

## Usage

To use this application, first install the necessary dependencies by running `pip install -r requirements.txt` in your terminal. Once the installation is complete, you can start the application by running `python run.py`.

## Files

- `app/views.py`: Contains the Flask routes and the main logic of the application.
- `app/templates/index.html`: The HTML template for the main page.
- `app/static/css/main.css`: The CSS styles for the application.
- `app/static/js/main.js`: The JavaScript code for handling form submission.
- `tests/test_views.py`: Contains unit tests for the application.

## Testing

To run the tests for this application, use the command `python -m unittest discover tests` in your terminal. This will run the tests defined in the `tests/test_views.py` file.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Temperature Display

The temperature is now displayed in Celsius.
