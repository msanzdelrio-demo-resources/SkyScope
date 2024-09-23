# Weather App

This is a simple weather application that allows users to get the current weather information for a specified city.

## Features

- Get current weather information for any city.
- Displays temperature, weather description, wind speed, and humidity.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/weather-app.git
    ```
2. Navigate to the project directory:
    ```sh
    cd weather-app
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

To use this application, first install the necessary dependencies by running `pip install -r requirements.txt` in your terminal. Once the installation is complete, you can start the application by running `python run.py`.

## Example Output

When you enter a city name, the application will display the following information:

- **City**: The name of the city.
- **Country**: The country where the city is located.
- **Temperature**: The current temperature in the city.
- **Description**: A brief description of the current weather.
- **Wind Speed**: The current wind speed in meters per second.
- **Humidity**: The current humidity percentage.

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