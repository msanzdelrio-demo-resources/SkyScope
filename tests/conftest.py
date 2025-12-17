"""
Test configuration and shared fixtures for SkyScope tests.

This module provides common test configuration, fixtures, and utilities
used across all test modules.
"""

import unittest
import tempfile
import os
from unittest.mock import patch, MagicMock

# Set environment variable for testing before importing app
# This prevents the ValueError in app/views.py when OPENWEATHER_APPID is not set
os.environ.setdefault('OPENWEATHER_APPID', 'test_api_key_for_testing')

from app import app


class BaseTestCase(unittest.TestCase):
    """Base test case providing common setup and teardown for all tests."""
    
    def setUp(self):
        """Set up test client and test environment."""
        self.app = app.test_client()
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SECRET_KEY'] = 'test-secret-key'
        
        # No database file needed for this application

    
    def tearDown(self):
        """Clean up after tests."""
        pass


class MockWeatherAPI:
    """Mock OpenWeatherMap API responses for testing."""
    
    @staticmethod
    def get_celsius_response():
        """Mock API response with Celsius temperatures."""
        return {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {
                'temp': 288.15,  # 15°C in Kelvin
                'feels_like': 286.15,  # 13°C in Kelvin
                'temp_min': 285.15,  # 12°C in Kelvin
                'temp_max': 291.15,  # 18°C in Kelvin
                'pressure': 1013,
                'humidity': 72
            },
            'weather': [
                {
                    'main': 'Clear',
                    'description': 'clear sky',
                    'icon': '01d'
                }
            ],
            'wind': {
                'speed': 3.6,
                'deg': 230
            },
            'rain': {},
            'clouds': {'all': 0}
        }
    
    @staticmethod
    def get_fahrenheit_response():
        """Mock API response with temperatures for Fahrenheit display."""
        return {
            'name': 'New York',
            'sys': {'country': 'US'},
            'main': {
                'temp': 298.15,  # 25°C in Kelvin (77°F)
                'feels_like': 301.15,  # 28°C in Kelvin (82.4°F)
                'temp_min': 295.15,  # 22°C in Kelvin (71.6°F)
                'temp_max': 301.15,  # 28°C in Kelvin (82.4°F)
                'pressure': 1015,
                'humidity': 65
            },
            'weather': [
                {
                    'main': 'Clouds',
                    'description': 'partly cloudy',
                    'icon': '03d'
                }
            ],
            'wind': {
                'speed': 4.1,
                'deg': 180
            },
            'rain': {'1h': 0.2},
            'clouds': {'all': 25}
        }
    
    @staticmethod
    def get_extreme_temperature_response():
        """Mock API response with extreme temperatures for edge case testing."""
        return {
            'name': 'Antarctica Research Station',
            'sys': {'country': 'AQ'},
            'main': {
                'temp': 233.15,  # -40°C in Kelvin (-40°F)
                'feels_like': 228.15,  # -45°C in Kelvin
                'temp_min': 223.15,  # -50°C in Kelvin
                'temp_max': 243.15,  # -30°C in Kelvin
                'pressure': 980,
                'humidity': 85
            },
            'weather': [
                {
                    'main': 'Snow',
                    'description': 'heavy snow',
                    'icon': '13d'
                }
            ],
            'wind': {
                'speed': 15.2,
                'deg': 45
            }
        }
    
    @staticmethod
    def get_hot_temperature_response():
        """Mock API response with very hot temperatures."""
        return {
            'name': 'Death Valley',
            'sys': {'country': 'US'},
            'main': {
                'temp': 323.15,  # 50°C in Kelvin (122°F)
                'feels_like': 328.15,  # 55°C in Kelvin
                'temp_min': 318.15,  # 45°C in Kelvin
                'temp_max': 328.15,  # 55°C in Kelvin
                'pressure': 1005,
                'humidity': 15
            },
            'weather': [
                {
                    'main': 'Clear',
                    'description': 'clear sky',
                    'icon': '01d'
                }
            ],
            'wind': {
                'speed': 2.1,
                'deg': 90
            }
        }


class TestDataFixtures:
    """Test data fixtures for temperature unit testing."""
    
    # Temperature conversion test cases
    TEMPERATURE_CONVERSIONS = [
        # (kelvin, celsius, fahrenheit, description)
        (273.15, 0.0, 32.0, "Water freezing point"),
        (373.15, 100.0, 212.0, "Water boiling point"),
        (288.15, 15.0, 59.0, "Room temperature"),
        (310.15, 37.0, 98.6, "Human body temperature"),
        (0.0, -273.15, -459.67, "Absolute zero"),
        (233.15, -40.0, -40.0, "Extreme cold"),
        (323.15, 50.0, 122.0, "Very hot day"),
    ]
    
    # Session test data
    SESSION_TEST_CASES = [
        {'unit': 'celsius', 'expected_symbol': '°C'},
        {'unit': 'fahrenheit', 'expected_symbol': '°F'},
        {'unit': 'kelvin', 'expected_symbol': 'K'},
    ]
    
    # API endpoint test data
    API_TEST_CITIES = [
        'London',
        'New York',
        'Tokyo',
        'Sydney',
        'Mumbai',
        'São Paulo',
        'Cairo',
        'Moscow'
    ]
    
    # Invalid input test cases
    INVALID_INPUTS = [
        '',  # Empty string
        '   ',  # Whitespace only
        'City123',  # Numbers
        'City!@#',  # Special characters
        'A' * 65,  # Too long
        '<script>alert("xss")</script>',  # XSS attempt
        "City'; DROP TABLE users; --",  # SQL injection attempt
        None,  # None value
        123,  # Non-string type
    ]
    
    @staticmethod
    def get_mock_weather_data(city, unit='celsius'):
        """Generate mock weather data for testing."""
        base_temp_k = 288.15  # 15°C in Kelvin
        
        if unit == 'celsius':
            temp = base_temp_k - 273.15
            symbol = '°C'
        elif unit == 'fahrenheit':
            temp = (base_temp_k - 273.15) * 9/5 + 32
            symbol = '°F'
        else:  # kelvin
            temp = base_temp_k
            symbol = 'K'
        
        return {
            'country': 'XX',
            'city': city,
            'temperature': round(temp, 1),
            'temperature_unit': unit,
            'temperature_symbol': symbol,
            'description': 'clear sky',
            'icon': '01d',
            'wind_speed': 5.2,
            'rain': 0,
            'pressure': 1013,
            'humidity': 65
        }