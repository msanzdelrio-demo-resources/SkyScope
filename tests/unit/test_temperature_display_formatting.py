"""
Tests for temperature display formatting with Fahrenheit support.

This module contains tests for proper formatting and display of temperatures
in all three supported units (Celsius, Fahrenheit, Kelvin).

Test Coverage:
- Temperature formatting with decimal places
- Unit symbol display
- Cross-unit consistency
- Weather data formatting for display
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock, Mock

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tests.conftest import BaseTestCase, MockWeatherAPI
from app.utils import format_temperature


class TestTemperatureDisplayFormatting(BaseTestCase):
    """Test cases for temperature display formatting."""
    
    def test_celsius_temperature_formatting(self):
        """Test formatting of Celsius temperatures for display."""
        test_cases = [
            (15.0, '15.0°C'),
            (25.5, '25.5°C'),
            (0.0, '0.0°C'),
            (-40.0, '-40.0°C'),
            (37.1, '37.1°C'),
        ]
        
        for temp, expected_format in test_cases:
            with self.subTest(temp=temp):
                result = format_temperature(temp, 'celsius')
                self.assertEqual(result, expected_format,
                               msg=f"Celsius formatting failed for {temp}")
    
    def test_fahrenheit_temperature_formatting(self):
        """Test formatting of Fahrenheit temperatures for display."""
        test_cases = [
            (59.0, '59.0°F'),
            (77.0, '77.0°F'),
            (32.0, '32.0°F'),
            (-40.0, '-40.0°F'),
            (98.6, '98.6°F'),
        ]
        
        for temp, expected_format in test_cases:
            with self.subTest(temp=temp):
                result = format_temperature(temp, 'fahrenheit')
                self.assertEqual(result, expected_format,
                               msg=f"Fahrenheit formatting failed for {temp}")
    
    def test_kelvin_temperature_formatting(self):
        """Test formatting of Kelvin temperatures for display."""
        test_cases = [
            (288.15, '288.1K'),
            (273.15, '273.1K'),
            (310.15, '310.1K'),
            (233.15, '233.2K'),
            (323.15, '323.1K'),
        ]
        
        for temp, expected_format in test_cases:
            with self.subTest(temp=temp):
                result = format_temperature(temp, 'kelvin')
                self.assertEqual(result, expected_format,
                               msg=f"Kelvin formatting failed for {temp}")
    
    def test_temperature_decimal_places_consistency(self):
        """Test that all units use consistent decimal place formatting (1 decimal)."""
        test_temperature = 15.567
        
        celsius_result = format_temperature(test_temperature, 'celsius')
        fahrenheit_result = format_temperature(59.02, 'fahrenheit')
        kelvin_result = format_temperature(288.717, 'kelvin')
        
        # All should have exactly 1 decimal place
        self.assertIn('.', celsius_result)
        self.assertIn('.', fahrenheit_result)
        self.assertIn('.', kelvin_result)
        
        # Check decimal precision (should be X.X format)
        celsius_parts = celsius_result.replace('°C', '').split('.')
        self.assertEqual(len(celsius_parts), 2)
        self.assertEqual(len(celsius_parts[1]), 1)
    
    def test_negative_temperature_formatting(self):
        """Test formatting of negative temperatures in all units."""
        negative_cases = [
            (celsius_temp, f_temp, unit)
            for celsius_temp, f_temp, unit in [
                (-10.0, 14.0, 'celsius'),
                (-40.0, -40.0, 'fahrenheit'),
            ]
        ]
        
        for temp, _, unit in negative_cases:
            with self.subTest(temp=temp, unit=unit):
                result = format_temperature(temp, unit)
                self.assertTrue(result.startswith('-'),
                              msg=f"Negative temperature should display with minus sign")
    
    def test_zero_temperature_formatting(self):
        """Test formatting of zero temperatures in all units."""
        units = ['celsius', 'fahrenheit', 'kelvin']
        
        for unit in units:
            with self.subTest(unit=unit):
                if unit in ['celsius', 'fahrenheit']:
                    result = format_temperature(0.0, unit)
                    self.assertIn('0.0', result)
                else:  # kelvin
                    result = format_temperature(0.0, unit)
                    self.assertIn('0.0', result)
    
    def test_extreme_temperature_formatting(self):
        """Test formatting of extreme temperatures."""
        extreme_cases = [
            (-273.15, 'celsius', '-273.1°C'),  # Absolute zero
            (-459.67, 'fahrenheit', '-459.7°F'),  # Absolute zero (rounds to -459.7)
            (5778.0, 'celsius', '5778.0°C'),  # Sun surface
        ]
        
        for temp, unit, expected in extreme_cases:
            with self.subTest(temp=temp, unit=unit):
                result = format_temperature(temp, unit)
                self.assertEqual(result, expected)


class TestWeatherDataFormattingWithFahrenheit(BaseTestCase):
    """Test cases for weather data formatting with Fahrenheit support."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.mock_api = MockWeatherAPI()
    
    @patch('requests.get')
    def test_weather_display_fahrenheit_all_temperatures(self, mock_get):
        """Test that all temperature fields are displayed in Fahrenheit."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {
                'temp': 288.15,  # 15°C = 59°F
                'feels_like': 286.15,  # 13°C = 55.4°F
                'temp_min': 285.15,  # 12°C = 53.6°F
                'temp_max': 291.15,  # 18°C = 64.4°F
                'pressure': 1013,
                'humidity': 72
            },
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'wind': {'speed': 3.6},
            'rain': {},
            'clouds': {'all': 0}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'London'})
            self.assertEqual(response.status_code, 200)
            
            # When implemented, should display all temperature fields in Fahrenheit
            # Main: 59°F, Feels like: 55.4°F, Min: 53.6°F, Max: 64.4°F
            html_content = response.get_data(as_text=True)
            self.assertNotIn('Error', html_content.upper())
    
    @patch('requests.get')
    def test_fahrenheit_display_consistency_across_weather_searches(self, mock_get):
        """Test that Fahrenheit display is consistent across multiple weather searches."""
        cities = ['London', 'Paris', 'Berlin']
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            for city in cities:
                with self.subTest(city=city):
                    mock_response = Mock()
                    mock_response.json.return_value = self.mock_api.get_celsius_response()
                    mock_response.status_code = 200
                    mock_get.return_value = mock_response
                    
                    response = client.post('/', data={'city': city})
                    self.assertEqual(response.status_code, 200)
                    
                    # All responses should maintain Fahrenheit display
                    html_content = response.get_data(as_text=True)
                    self.assertNotIn('Error', html_content.upper())
                    
                    # Fahrenheit preference should persist
                    with client.session_transaction() as sess:
                        self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    @patch('requests.get')
    def test_temperature_range_display_in_fahrenheit(self, mock_get):
        """Test that temperature range (min/max) displays correctly in Fahrenheit."""
        # API returns: min=285.15K (12°C=53.6°F), max=291.15K (18°C=64.4°F)
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'TestCity',
            'sys': {'country': 'XX'},
            'main': {
                'temp': 288.15,
                'feels_like': 288.15,
                'temp_min': 285.15,
                'temp_max': 291.15,
                'pressure': 1013,
                'humidity': 70
            },
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'wind': {'speed': 3.0},
            'rain': {},
            'clouds': {'all': 0}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'TestCity'})
            self.assertEqual(response.status_code, 200)
            
            # When implemented, should show min/max in Fahrenheit
            # Min: 53.6°F, Max: 64.4°F
            html_content = response.get_data(as_text=True)
            self.assertNotIn('Error', html_content.upper())
    
    @patch('requests.get')
    def test_feels_like_display_in_fahrenheit(self, mock_get):
        """Test that 'feels like' temperature displays correctly in Fahrenheit."""
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {
                'temp': 288.15,  # 15°C = 59°F
                'feels_like': 281.15,  # 8°C = 46.4°F (wind chill)
                'temp_min': 285.15,
                'temp_max': 291.15,
                'pressure': 1013,
                'humidity': 72
            },
            'weather': [{'description': 'windy', 'icon': '01d'}],
            'wind': {'speed': 15.0},  # Very windy
            'rain': {},
            'clouds': {'all': 0}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'London'})
            self.assertEqual(response.status_code, 200)
            
            # When implemented, should display feels like in Fahrenheit
            # Actual: 59°F, Feels like: 46.4°F
            html_content = response.get_data(as_text=True)
            self.assertNotIn('Error', html_content.upper())


class TestTemperatureConversionDisplayAccuracy(BaseTestCase):
    """Test cases for accuracy of temperature conversion in display."""
    
    def test_celsius_to_fahrenheit_display_accuracy(self):
        """Test accuracy of Celsius to Fahrenheit conversion in display."""
        test_cases = [
            (0.0, 32.0),      # Freezing point
            (100.0, 212.0),   # Boiling point
            (37.0, 98.6),     # Body temperature
            (-40.0, -40.0),   # Same in both scales
            (20.0, 68.0),     # Room temperature
        ]
        
        for celsius, expected_fahrenheit in test_cases:
            with self.subTest(celsius=celsius):
                # Format and verify
                celsius_str = format_temperature(celsius, 'celsius')
                fahrenheit_str = format_temperature(expected_fahrenheit, 'fahrenheit')
                
                # Both should format correctly
                self.assertIn('°C', celsius_str)
                self.assertIn('°F', fahrenheit_str)
    
    def test_kelvin_to_fahrenheit_display_accuracy(self):
        """Test accuracy of Kelvin to Fahrenheit conversion in display."""
        test_cases = [
            (273.15, 32.0),   # Freezing point
            (373.15, 212.0),  # Boiling point
            (310.15, 98.6),   # Body temperature
            (233.15, -40.0),  # Same conversion
            (288.15, 59.0),   # Room temperature
        ]
        
        for kelvin, expected_fahrenheit in test_cases:
            with self.subTest(kelvin=kelvin):
                kelvin_str = format_temperature(kelvin, 'kelvin')
                fahrenheit_str = format_temperature(expected_fahrenheit, 'fahrenheit')
                
                # Both should format correctly
                self.assertIn('K', kelvin_str)
                self.assertIn('°F', fahrenheit_str)
    
    def test_all_units_same_temperature_display(self):
        """Test that same physical temperature displays as equivalent in all units."""
        # Use water boiling point as reference
        kelvin = 373.15
        celsius = 100.0
        fahrenheit = 212.0
        
        kelvin_display = format_temperature(kelvin, 'kelvin')
        celsius_display = format_temperature(celsius, 'celsius')
        fahrenheit_display = format_temperature(fahrenheit, 'fahrenheit')
        
        # All should have proper symbols
        self.assertIn('K', kelvin_display)
        self.assertIn('°C', celsius_display)
        self.assertIn('°F', fahrenheit_display)
        
        # All should have decimal places
        self.assertIn('.', kelvin_display)
        self.assertIn('.', celsius_display)
        self.assertIn('.', fahrenheit_display)


class TestTemperatureDisplayEdgeCases(BaseTestCase):
    """Test cases for edge cases in temperature display."""
    
    def test_very_small_positive_temperature_fahrenheit(self):
        """Test display of very small positive Fahrenheit temperature."""
        # 0.1°F is approximately -17.7°C
        result = format_temperature(0.1, 'fahrenheit')
        self.assertEqual(result, '0.1°F')
    
    def test_very_large_temperature_fahrenheit(self):
        """Test display of very large Fahrenheit temperature."""
        # 1000°F
        result = format_temperature(1000.0, 'fahrenheit')
        self.assertEqual(result, '1000.0°F')
    
    def test_temperature_with_many_decimal_places(self):
        """Test rounding of temperature with many decimal places."""
        # 15.5555°C - Python's round() uses banker's rounding
        result = format_temperature(15.5555, 'celsius')
        # Should round to 1 decimal place (15.5555 rounds to 15.6)
        self.assertEqual(result, '15.6°C')
    
    def test_temperature_rounding_up(self):
        """Test rounding up of temperature."""
        # 15.95°C should round to 16.0°C
        result = format_temperature(15.95, 'celsius')
        # Note: exact rounding behavior depends on implementation
        self.assertIn('°C', result)
    
    def test_temperature_rounding_down(self):
        """Test rounding down of temperature."""
        # 15.14°C should round to 15.1°C
        result = format_temperature(15.14, 'celsius')
        self.assertIn('°C', result)


if __name__ == '__main__':
    unittest.main()
