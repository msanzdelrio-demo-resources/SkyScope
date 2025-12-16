"""
Test fixtures and sample data for temperature unit testing.

This module provides comprehensive test data, mock responses,
and fixtures for testing temperature-related functionality
across all test suites.
"""

import json
import datetime
from typing import Dict, List, Any, Optional


class WeatherDataFixtures:
    """Fixtures for weather data with different temperature units and scenarios."""
    
    # Real-world temperature data for major cities (in Kelvin from OpenWeatherMap)
    CITY_TEMPERATURES = {
        'London': {
            'kelvin': 288.15,  # 15°C, 59°F
            'city': 'London',
            'country': 'GB',
            'description': 'partly cloudy',
            'icon': '03d',
            'humidity': 72,
            'pressure': 1013,
            'wind_speed': 4.1,
            'wind_deg': 230
        },
        'New York': {
            'kelvin': 298.15,  # 25°C, 77°F
            'city': 'New York',
            'country': 'US',
            'description': 'clear sky',
            'icon': '01d',
            'humidity': 65,
            'pressure': 1015,
            'wind_speed': 3.6,
            'wind_deg': 180
        },
        'Tokyo': {
            'kelvin': 301.15,  # 28°C, 82.4°F
            'city': 'Tokyo',
            'country': 'JP',
            'description': 'light rain',
            'icon': '10d',
            'humidity': 78,
            'pressure': 1011,
            'wind_speed': 2.8,
            'wind_deg': 45,
            'rain': {'1h': 0.5}
        },
        'Sydney': {
            'kelvin': 293.15,  # 20°C, 68°F
            'city': 'Sydney',
            'country': 'AU',
            'description': 'few clouds',
            'icon': '02d',
            'humidity': 68,
            'pressure': 1018,
            'wind_speed': 5.2,
            'wind_deg': 120
        },
        'Mumbai': {
            'kelvin': 308.15,  # 35°C, 95°F
            'city': 'Mumbai',
            'country': 'IN',
            'description': 'haze',
            'icon': '50d',
            'humidity': 85,
            'pressure': 1008,
            'wind_speed': 1.5,
            'wind_deg': 270
        },
        'Moscow': {
            'kelvin': 268.15,  # -5°C, 23°F
            'city': 'Moscow',
            'country': 'RU',
            'description': 'snow',
            'icon': '13d',
            'humidity': 88,
            'pressure': 998,
            'wind_speed': 6.7,
            'wind_deg': 315,
            'snow': {'1h': 2.1}
        },
        'Reykjavik': {
            'kelvin': 275.15,  # 2°C, 35.6°F
            'city': 'Reykjavik',
            'country': 'IS',
            'description': 'overcast clouds',
            'icon': '04d',
            'humidity': 91,
            'pressure': 985,
            'wind_speed': 8.2,
            'wind_deg': 200
        },
        'Dubai': {
            'kelvin': 313.15,  # 40°C, 104°F
            'city': 'Dubai',
            'country': 'AE',
            'description': 'clear sky',
            'icon': '01d',
            'humidity': 45,
            'pressure': 1012,
            'wind_speed': 4.6,
            'wind_deg': 90
        }
    }
    
    # Extreme weather scenarios for edge case testing
    EXTREME_WEATHER_SCENARIOS = {
        'death_valley': {
            'kelvin': 328.15,  # 55°C, 131°F
            'city': 'Death Valley',
            'country': 'US',
            'description': 'clear sky',
            'icon': '01d',
            'humidity': 10,
            'pressure': 1005,
            'wind_speed': 2.1,
            'wind_deg': 90
        },
        'antarctica': {
            'kelvin': 223.15,  # -50°C, -58°F
            'city': 'McMurdo Station',
            'country': 'AQ',
            'description': 'heavy snow',
            'icon': '13d',
            'humidity': 95,
            'pressure': 980,
            'wind_speed': 25.2,
            'wind_deg': 45,
            'snow': {'1h': 5.0}
        },
        'sahara': {
            'kelvin': 323.15,  # 50°C, 122°F
            'city': 'Sahara Desert',
            'country': 'DZ',
            'description': 'dust',
            'icon': '50d',
            'humidity': 15,
            'pressure': 1008,
            'wind_speed': 12.3,
            'wind_deg': 120
        },
        'siberia': {
            'kelvin': 233.15,  # -40°C, -40°F
            'city': 'Verkhoyansk',
            'country': 'RU',
            'description': 'clear sky',
            'icon': '01n',
            'humidity': 89,
            'pressure': 995,
            'wind_speed': 1.2,
            'wind_deg': 180
        }
    }
    
    @classmethod
    def get_openweather_api_response(cls, city_key: str, units: str = 'standard') -> Dict[str, Any]:
        """
        Generate OpenWeatherMap API response format for a given city.
        
        Args:
            city_key: Key from CITY_TEMPERATURES or EXTREME_WEATHER_SCENARIOS
            units: API units parameter ('standard', 'metric', 'imperial')
        
        Returns:
            Dict matching OpenWeatherMap API response format
        """
        # Get base data
        if city_key in cls.CITY_TEMPERATURES:
            data = cls.CITY_TEMPERATURES[city_key].copy()
        elif city_key in cls.EXTREME_WEATHER_SCENARIOS:
            data = cls.EXTREME_WEATHER_SCENARIOS[city_key].copy()
        else:
            raise ValueError(f"Unknown city key: {city_key}")
        
        # Convert temperature based on units
        kelvin_temp = data['kelvin']
        if units == 'metric':
            temp = kelvin_temp - 273.15  # Celsius
            feels_like = temp - 2  # Simulate feels like
        elif units == 'imperial':
            temp = (kelvin_temp - 273.15) * 9/5 + 32  # Fahrenheit
            feels_like = temp - 3  # Simulate feels like
        else:  # standard (Kelvin)
            temp = kelvin_temp
            feels_like = temp - 2
        
        # Build API response
        response = {
            'coord': {'lon': 0.0, 'lat': 0.0},  # Simplified coordinates
            'weather': [{
                'id': 800,
                'main': data['description'].split()[0].title(),
                'description': data['description'],
                'icon': data['icon']
            }],
            'base': 'stations',
            'main': {
                'temp': round(temp, 2),
                'feels_like': round(feels_like, 2),
                'temp_min': round(temp - 3, 2),
                'temp_max': round(temp + 2, 2),
                'pressure': data['pressure'],
                'humidity': data['humidity']
            },
            'visibility': 10000,
            'wind': {
                'speed': data['wind_speed'],
                'deg': data['wind_deg']
            },
            'clouds': {'all': 20},
            'dt': 1640995200,  # Fixed timestamp for consistent testing
            'sys': {
                'type': 2,
                'id': 2000000,
                'country': data['country'],
                'sunrise': 1640995200,
                'sunset': 1641031200
            },
            'timezone': 0,
            'id': 1000000,
            'name': data['city'],
            'cod': 200
        }
        
        # Add optional weather conditions
        if 'rain' in data:
            response['rain'] = data['rain']
        if 'snow' in data:
            response['snow'] = data['snow']
        
        return response
    
    @classmethod
    def get_processed_weather_data(cls, city_key: str, unit: str = 'celsius') -> Dict[str, Any]:
        """
        Get weather data as it would be processed by the application.
        
        Args:
            city_key: City identifier
            unit: Temperature unit ('celsius', 'fahrenheit', 'kelvin')
        
        Returns:
            Processed weather data dict
        """
        if city_key in cls.CITY_TEMPERATURES:
            data = cls.CITY_TEMPERATURES[city_key].copy()
        elif city_key in cls.EXTREME_WEATHER_SCENARIOS:
            data = cls.EXTREME_WEATHER_SCENARIOS[city_key].copy()
        else:
            raise ValueError(f"Unknown city key: {city_key}")
        
        kelvin_temp = data['kelvin']
        
        # Convert temperature
        if unit == 'celsius':
            temp = kelvin_temp - 273.15
            symbol = '°C'
        elif unit == 'fahrenheit':
            temp = (kelvin_temp - 273.15) * 9/5 + 32
            symbol = '°F'
        else:  # kelvin
            temp = kelvin_temp
            symbol = 'K'
        
        return {
            'country': data['country'],
            'city': data['city'],
            'temperature': round(temp, 1),
            'temperature_unit': unit,
            'temperature_symbol': symbol,
            'description': data['description'],
            'icon': data['icon'],
            'wind_speed': data['wind_speed'],
            'rain': data.get('rain', {}).get('1h', 0),
            'pressure': data['pressure'],
            'humidity': data['humidity']
        }


class TemperatureConversionFixtures:
    """Fixtures for temperature conversion testing."""
    
    # Precise temperature conversion test cases
    CONVERSION_TEST_CASES = [
        {
            'kelvin': 0.0,
            'celsius': -273.15,
            'fahrenheit': -459.67,
            'description': 'Absolute zero'
        },
        {
            'kelvin': 273.15,
            'celsius': 0.0,
            'fahrenheit': 32.0,
            'description': 'Water freezing point'
        },
        {
            'kelvin': 373.15,
            'celsius': 100.0,
            'fahrenheit': 212.0,
            'description': 'Water boiling point'
        },
        {
            'kelvin': 288.15,
            'celsius': 15.0,
            'fahrenheit': 59.0,
            'description': 'Room temperature'
        },
        {
            'kelvin': 310.15,
            'celsius': 37.0,
            'fahrenheit': 98.6,
            'description': 'Human body temperature'
        },
        {
            'kelvin': 255.37,
            'celsius': -17.78,
            'fahrenheit': 0.0,
            'description': 'Fahrenheit zero point'
        },
        {
            'kelvin': 233.15,
            'celsius': -40.0,
            'fahrenheit': -40.0,
            'description': 'Celsius-Fahrenheit intersection'
        }
    ]
    
    # Edge cases for temperature conversion
    EDGE_CASES = [
        {
            'kelvin': 0.01,
            'celsius': -273.14,
            'fahrenheit': -459.652,
            'description': 'Near absolute zero'
        },
        {
            'kelvin': 1000.0,
            'celsius': 726.85,
            'fahrenheit': 1340.33,
            'description': 'Very hot temperature'
        },
        {
            'kelvin': 5778.0,
            'celsius': 5504.85,
            'fahrenheit': 9940.73,
            'description': 'Surface of the Sun'
        },
        {
            'kelvin': 2.725,
            'celsius': -270.425,
            'fahrenheit': -454.765,
            'description': 'Cosmic microwave background'
        }
    ]
    
    @classmethod
    def get_conversion_test_data(cls, include_edge_cases: bool = True) -> List[Dict[str, Any]]:
        """Get all temperature conversion test data."""
        data = cls.CONVERSION_TEST_CASES.copy()
        if include_edge_cases:
            data.extend(cls.EDGE_CASES)
        return data


class APIErrorFixtures:
    """Fixtures for API error scenarios and responses."""
    
    # Common API error responses
    ERROR_RESPONSES = {
        'city_not_found': {
            'status_code': 404,
            'response': {
                'cod': '404',
                'message': 'city not found'
            }
        },
        'invalid_api_key': {
            'status_code': 401,
            'response': {
                'cod': 401,
                'message': 'Invalid API key. Please see http://openweathermap.org/faq#error401 for more info.'
            }
        },
        'rate_limit_exceeded': {
            'status_code': 429,
            'response': {
                'cod': 429,
                'message': 'Your account is temporary blocked due to exceeding of requests limitation of your subscription type.'
            }
        },
        'server_error': {
            'status_code': 500,
            'response': {
                'cod': 500,
                'message': 'Internal error'
            }
        },
        'service_unavailable': {
            'status_code': 503,
            'response': {
                'cod': 503,
                'message': 'Service temporary unavailable'
            }
        }
    }
    
    # Network error scenarios
    NETWORK_ERRORS = [
        'requests.exceptions.ConnectionError',
        'requests.exceptions.Timeout',
        'requests.exceptions.RequestException',
        'requests.exceptions.HTTPError'
    ]
    
    @classmethod
    def get_error_response(cls, error_type: str) -> Dict[str, Any]:
        """Get API error response for testing."""
        if error_type in cls.ERROR_RESPONSES:
            return cls.ERROR_RESPONSES[error_type]
        raise ValueError(f"Unknown error type: {error_type}")


class SessionTestFixtures:
    """Fixtures for session management testing."""
    
    # Valid session data
    VALID_SESSION_DATA = [
        {'temperature_unit': 'celsius'},
        {'temperature_unit': 'fahrenheit'},
        {'temperature_unit': 'kelvin'},
        {'temperature_unit': 'celsius', 'other_data': 'preserved'},
        {'temperature_unit': 'fahrenheit', 'user_preferences': {'theme': 'dark'}}
    ]
    
    # Invalid session data for security testing
    INVALID_SESSION_DATA = [
        {'temperature_unit': '<script>alert("xss")</script>'},
        {'temperature_unit': '"; DROP TABLE sessions; --'},
        {'temperature_unit': '../../../etc/passwd'},
        {'temperature_unit': 'celsius' + 'x' * 1000},  # Too long
        {'temperature_unit': {'invalid': 'object'}},
        {'temperature_unit': None},
        {'temperature_unit': 123},
        {'temperature_unit': []},
    ]
    
    # Unicode test data
    UNICODE_SESSION_DATA = [
        {'temperature_unit': 'célsius'},
        {'temperature_unit': 'fahrenheit™'},
        {'temperature_unit': '开尔文'},  # Chinese
        {'temperature_unit': 'кельвин'},  # Russian
        {'temperature_unit': '🌡️celsius'},  # With emoji
    ]


class UITestFixtures:
    """Fixtures for UI and frontend testing."""
    
    # Expected HTML elements for temperature toggle
    EXPECTED_HTML_ELEMENTS = [
        '<div class="temperature-toggle">',
        '<input type="radio" name="temperature-unit" value="celsius">',
        '<input type="radio" name="temperature-unit" value="fahrenheit">',
        '<input type="radio" name="temperature-unit" value="kelvin">',
        '<label for="celsius">°C</label>',
        '<label for="fahrenheit">°F</label>',
        '<label for="kelvin">K</label>',
    ]
    
    # ARIA attributes for accessibility
    ACCESSIBILITY_ATTRIBUTES = [
        'aria-label="Temperature unit selection"',
        'role="radiogroup"',
        'tabindex="0"',
        'aria-describedby="temp-unit-description"',
    ]
    
    # CSS classes for styling
    CSS_CLASSES = [
        'temperature-toggle',
        'toggle-switch',
        'unit-selector',
        'temperature-display',
        'unit-symbol',
        'active',
        'selected'
    ]
    
    # JavaScript function names
    JS_FUNCTIONS = [
        'toggleTemperatureUnit',
        'updateTemperatureDisplay',
        'handleUnitChange',
        'setTemperatureUnit',
        'convertTemperature'
    ]


class PerformanceTestFixtures:
    """Fixtures for performance testing."""
    
    # Performance benchmarks
    PERFORMANCE_BENCHMARKS = {
        'temperature_conversion_time_ms': 10.0,
        'page_load_time_s': 1.0,
        'ajax_response_time_ms': 500.0,
        'api_response_time_ms': 3000.0,
        'javascript_execution_time_ms': 100.0
    }
    
    # Load testing data
    LOAD_TEST_SCENARIOS = [
        {'concurrent_users': 1, 'requests_per_second': 1},
        {'concurrent_users': 10, 'requests_per_second': 5},
        {'concurrent_users': 100, 'requests_per_second': 20},
        {'concurrent_users': 1000, 'requests_per_second': 50}
    ]


class CrossBrowserTestFixtures:
    """Fixtures for cross-browser compatibility testing."""
    
    # Browser user agents for testing
    BROWSER_USER_AGENTS = {
        'chrome': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'firefox': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'safari': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'edge': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
        'mobile_chrome': 'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
        'mobile_safari': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    }
    
    # Feature support matrix for different browsers
    BROWSER_FEATURES = {
        'css_grid': ['chrome', 'firefox', 'safari', 'edge'],
        'flexbox': ['chrome', 'firefox', 'safari', 'edge', 'mobile_chrome', 'mobile_safari'],
        'es6_modules': ['chrome', 'firefox', 'safari', 'edge'],
        'custom_properties': ['chrome', 'firefox', 'safari', 'edge'],
        'fetch_api': ['chrome', 'firefox', 'safari', 'edge', 'mobile_chrome', 'mobile_safari']
    }


# Export all fixtures as a convenience
__all__ = [
    'WeatherDataFixtures',
    'TemperatureConversionFixtures',
    'APIErrorFixtures',
    'SessionTestFixtures',
    'UITestFixtures',
    'PerformanceTestFixtures',
    'CrossBrowserTestFixtures'
]