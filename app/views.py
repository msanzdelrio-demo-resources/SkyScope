from flask import render_template, request, session, jsonify
from . import app
from .utils import convert_weather_data, format_temperature, convert_temperature
import requests
import os
import re
import secrets
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Secure API key configuration
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_APPID')
if not OPENWEATHER_API_KEY and not app.config.get('TESTING'):
    raise ValueError("OPENWEATHER_APPID environment variable is required")

# Secure secret key configuration
secret_key = os.environ.get('SECRET_KEY')
if not secret_key:
    # Generate a secure random secret key for development
    secret_key = secrets.token_hex(32)
    print(f"WARNING: Using generated secret key. Set SECRET_KEY environment variable for production.")
app.secret_key = secret_key


def get_temperature_unit() -> str:
    """Get current temperature unit from session, defaulting to Celsius."""
    unit = session.get('temperature_unit', 'celsius')
    # Ensure we return a valid string and handle edge cases
    if not isinstance(unit, str):
        return 'celsius'
    unit = unit.lower()
    # Only return valid unit values to prevent XSS
    if unit in {'celsius', 'kelvin', 'fahrenheit'}:
        return unit
    return 'celsius'


def set_temperature_unit(unit: str) -> bool:
    """
    Set temperature unit in session with validation.
    
    Args:
        unit: Temperature unit to set
        
    Returns:
        True if unit was set successfully, False otherwise
    """
    unit = unit.lower().strip()
    if unit in {'celsius', 'kelvin', 'fahrenheit'}:
        session['temperature_unit'] = unit
        session.permanent = True
        return True
    return False


def get_api_units_parameter(temperature_unit: str) -> str:
    """
    Convert temperature unit preference to OpenWeatherMap API units parameter.
    
    Args:
        temperature_unit: User's preferred temperature unit (celsius, kelvin, fahrenheit)
        
    Returns:
        API units parameter: 'metric' for Celsius, 'standard' for Kelvin, 'imperial' for Fahrenheit
    """
    unit_map = {
        'celsius': 'metric',
        'kelvin': 'standard',
        'fahrenheit': 'imperial'
    }
    return unit_map.get(temperature_unit.lower(), 'metric')


def get_mock_weather_data(city: str) -> Dict[str, Any]:
    """Return mock weather data for testing purposes."""
    return {
        'country': 'XX',
        'city': city,
        'temperature': 15.5,
        'description': 'clear sky',
        'icon': '01d',
        'wind_speed': 5.2,
        'rain': 0,
        'pressure': 1013,
        'feels_like': 14.2,
        'temp_min': 12.0,
        'temp_max': 18.0
    }


def fetch_weather_data(city: str, units: Optional[str] = 'metric') -> Optional[Dict[str, Any]]:
    """
    Fetch weather data from OpenWeatherMap API.
    
    Args:
        city: City name to fetch weather for
        units: API units parameter ('standard', 'metric', 'imperial'), or None for default (Kelvin)
        
    Returns:
        Weather data dictionary or None if request fails
    """
    try:
        # Use HTTPS for secure communication
        # Build URL with optional units parameter
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}'
        if units and units != 'standard':
            url += f'&units={units}'
        
        response = requests.get(url, timeout=10, verify=True)
        response.raise_for_status()
        
        api_data = response.json()
        
        # Extract and structure weather data
        weather_data = {
            'country': api_data['sys']['country'],
            'city': api_data['name'],
            'temperature': api_data['main']['temp'],
            'feels_like': api_data['main']['feels_like'], 
            'temp_min': api_data['main']['temp_min'],
            'temp_max': api_data['main']['temp_max'],
            'description': api_data['weather'][0]['description'],
            'icon': api_data['weather'][0]['icon'],
            'wind_speed': api_data['wind']['speed'],
            'rain': api_data.get('rain', {}).get('1h', 0),
            'pressure': api_data['main']['pressure']
        }
        
        return weather_data
        
    except (requests.RequestException, KeyError, ValueError) as e:
        # Sanitize user input before logging to prevent log injection
        safe_city = city.replace('\r', '').replace('\n', '')[:20]
        app.logger.error(f"Weather API error for city '{safe_city}...': {type(e).__name__}")
        return None


@app.route('/set-temperature-unit', methods=['POST'])
def set_temperature_unit_endpoint():
    """Endpoint to set temperature unit preference in session."""
    try:
        # Handle both JSON and form data with input validation
        if request.is_json:
            unit = request.json.get('unit', '').strip() if request.json else ''
        else:
            unit = request.form.get('unit', '').strip()
        
        # Validate input exists and is not empty
        if not unit:
            return jsonify({'error': 'Temperature unit is required'}), 400
        
        # Additional validation for expected values only
        valid_units = {'celsius', 'kelvin', 'fahrenheit'}
        if unit.lower() not in valid_units:
            return jsonify({
                'error': 'Invalid temperature unit. Must be celsius, fahrenheit, or kelvin'
            }), 400
        
        # Validate and set temperature unit
        if set_temperature_unit(unit):
            return jsonify({
                'success': True,
                'unit': unit,
                'message': f'Temperature unit set to {unit.title()}'
            })
        else:
            return jsonify({
                'error': 'Invalid temperature unit. Must be celsius, fahrenheit, or kelvin'
            }), 400
            
    except Exception as e:
        # Log error without exposing details
        app.logger.error(f"Error setting temperature unit: {type(e).__name__}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error_message = None

    # Get current temperature unit preference
    temp_unit = get_temperature_unit()

    if request.method == 'POST':
        city = request.form.get('city', '').strip()

        # Improved city name validation to include numbers and international characters
        # Allow letters, spaces, hyphens, apostrophes, commas, periods, and numbers
        if not city:
            error_message = "Please enter a city name"
        elif not re.match(r"^[a-zA-Z\s\-',.0-9]{1,64}$", city):
            error_message = "Invalid city name format. Please use only letters, numbers, spaces, and basic punctuation."
        else:
            # Use mock data when in testing mode
            if app.testing:
                weather = get_mock_weather_data(city)
                # Mock data is in Celsius
                source_unit = 'celsius'
            else:
                # Fetch weather data from API with appropriate units
                api_units = get_api_units_parameter(temp_unit)
                weather = fetch_weather_data(city, api_units)
                
                if not weather:
                    error_message = "Unable to fetch weather data. Please try again."
                
                # Determine source unit from API units parameter
                # API returns temperatures in the unit specified by the units parameter
                if api_units == 'metric':
                    source_unit = 'celsius'
                elif api_units == 'imperial':
                    source_unit = 'fahrenheit'
                else:  # standard or None
                    source_unit = 'kelvin'

            # Convert temperature data to user's preferred unit if needed
            if weather:
                try:
                    # Only convert if source and target units differ
                    if source_unit != temp_unit:
                        weather = convert_weather_data(weather, temp_unit, source_unit=source_unit)
                    
                    # Format temperature displays with units
                    weather['temperature_formatted'] = format_temperature(weather['temperature'], temp_unit)
                    weather['feels_like_formatted'] = format_temperature(weather['feels_like'], temp_unit) 
                    weather['temp_min_formatted'] = format_temperature(weather['temp_min'], temp_unit)
                    weather['temp_max_formatted'] = format_temperature(weather['temp_max'], temp_unit)
                    
                except (ValueError, TypeError) as e:
                    app.logger.error(f"Error converting temperature data: {e}")
                    error_message = "Error processing temperature data"
                    weather = None

    return render_template('index.html', 
                         weather=weather, 
                         error=error_message,
                         temperature_unit=temp_unit)
