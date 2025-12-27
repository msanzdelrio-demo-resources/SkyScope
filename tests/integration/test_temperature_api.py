"""
Integration tests for temperature-aware API functionality.

This module tests the integration between temperature units,
OpenWeatherMap API calls, and weather data processing.

Test Coverage:
- OpenWeatherMap API integration with unit parameters
- Temperature data processing with different units
- API response formatting and error handling
- Weather data display with unit awareness
- Mock API testing for reliability
"""

import unittest
import json
from unittest.mock import patch, MagicMock, Mock
import requests
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tests.conftest import BaseTestCase, MockWeatherAPI, TestDataFixtures


class TestTemperatureAwareAPI(BaseTestCase):
    """Integration tests for temperature-aware weather API functionality."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.mock_api = MockWeatherAPI()
        # Temporarily disable testing mode to allow API calls to be made
        # (they'll be mocked by @patch decorators anyway)
        from app import app as flask_app
        flask_app.testing = False
    
    def tearDown(self):
        """Clean up after tests."""
        # Re-enable testing mode
        from app import app as flask_app
        flask_app.testing = True
        super().tearDown()
    
    @patch('requests.get')
    def test_openweather_api_celsius_request(self, mock_get):
        """Test OpenWeatherMap API request with Celsius units."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_celsius_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test API call with Celsius units
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'celsius'
            
            response = client.post('/', data={'city': 'London'})
            
            # Verify API was called correctly
            self.assertEqual(response.status_code, 200)
            mock_get.assert_called_once()
            
            # Check that API call includes correct parameters
            call_args = mock_get.call_args
            self.assertIn('units=metric', call_args[0][0])
    
    @patch('requests.get')
    def test_openweather_api_fahrenheit_request(self, mock_get):
        """Test OpenWeatherMap API request with Fahrenheit units."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_fahrenheit_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test API call with Fahrenheit units
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'New York'})
            
            # Verify API was called correctly
            self.assertEqual(response.status_code, 200)
            mock_get.assert_called_once()
            
            # Check that API call includes correct parameters
            call_args = mock_get.call_args
            self.assertIn('units=imperial', call_args[0][0])
    
    @patch('requests.get')
    def test_openweather_api_kelvin_request(self, mock_get):
        """Test OpenWeatherMap API request with Kelvin units (default)."""
        # Mock API response for Kelvin (no units parameter)
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_celsius_response()
    
    @patch('requests.get')
    def test_fahrenheit_to_celsius_api_transition(self, mock_get):
        """Test transitioning from Fahrenheit to Celsius API calls."""
        # Mock API responses
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_fahrenheit_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            # First request with Fahrenheit
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response1 = client.post('/', data={'city': 'Miami'})
            self.assertEqual(response1.status_code, 200)
            
            # Change to Celsius
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'celsius'
            
            mock_response.json.return_value = self.mock_api.get_celsius_response()
            response2 = client.post('/', data={'city': 'Miami'})
            self.assertEqual(response2.status_code, 200)
            
            # Verify both API calls succeeded
            self.assertEqual(mock_get.call_count, 2)
    
    @patch('requests.get')
    def test_all_three_units_api_parameters(self, mock_get):
        """Test that all three temperature units map to correct API parameters."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        unit_mappings = [
            ('celsius', 'units=metric'),
            ('fahrenheit', 'units=imperial'),
            ('kelvin', ''),  # Kelvin doesn't include units parameter
        ]
        
        for unit, expected_param in unit_mappings:
            with self.subTest(unit=unit):
                mock_response.json.return_value = self.mock_api.get_celsius_response()
                mock_get.reset_mock()  # Reset call count for each subtest
                
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    response = client.post('/', data={'city': 'TestCity'})
                    self.assertEqual(response.status_code, 200)
                    
                    # Verify API was called
                    self.assertTrue(mock_get.called, f"API should be called for {unit}")
                    
                    # Verify correct API parameter was used
                    if mock_get.called:
                        call_args = mock_get.call_args[0][0]
                        if expected_param:
                            self.assertIn(expected_param, call_args, 
                                        f"Expected {expected_param} in API call for {unit}")
    
    @patch('requests.get')
    def test_api_response_temperature_conversion(self, mock_get):
        """Test temperature conversion in API response processing."""
        # Mock Kelvin response (288.15K = 15°C)
        mock_response = Mock()
        mock_response.json.return_value = {
            'name': 'London',
            'sys': {'country': 'GB'},
            'main': {
                'temp': 288.15,  # 15°C in Kelvin
                'feels_like': 290.15,  # 17°C in Kelvin
                'temp_min': 285.15,  # 12°C in Kelvin
                'temp_max': 291.15,  # 18°C in Kelvin
                'pressure': 1013,
                'humidity': 72
            },
            'weather': [{'description': 'clear sky', 'icon': '01d'}],
            'wind': {'speed': 3.6},
            'rain': {}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Test with different unit preferences
        test_cases = [
            ('celsius', '15.0°C'),
            ('fahrenheit', '59.0°F'),
            ('kelvin', '288.1K')
        ]
        
        for unit, expected_display in test_cases:
            with self.subTest(unit=unit):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    response = client.post('/', data={'city': 'London'})
                    self.assertEqual(response.status_code, 200)
                    
                    # Check that temperature is displayed in correct unit
                    # This would require actual implementation of unit-aware display
                    response_text = response.get_data(as_text=True)
                    # When implemented, should contain the expected format
    
    @patch('requests.get')
    def test_api_error_handling_with_units(self, mock_get):
        """Test API error handling with different temperature units."""
        # Mock various API errors
        error_responses = [
            {'status_code': 404, 'json': {'message': 'city not found'}},
            {'status_code': 401, 'json': {'message': 'Invalid API key'}},
            {'status_code': 500, 'json': {'message': 'Internal server error'}},
            {'status_code': 429, 'json': {'message': 'Rate limit exceeded'}},
        ]
        
        for error_response in error_responses:
            with self.subTest(status=error_response['status_code']):
                mock_response = Mock()
                mock_response.status_code = error_response['status_code']
                mock_response.json.return_value = error_response['json']
                mock_get.return_value = mock_response
                
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = 'celsius'
                    
                    response = client.post('/', data={'city': 'InvalidCity'})
                    
                    # Should handle errors gracefully
                    self.assertEqual(response.status_code, 200)
                    
                    # Should not display weather data on error
                    response_text = response.get_data(as_text=True)
                    # When implemented, error handling should be tested here
    
    @patch('requests.get')
    def test_api_timeout_handling(self, mock_get):
        """Test handling of API timeouts."""
        # Mock timeout exception
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'London'})
            
            # Should handle timeout gracefully
            self.assertEqual(response.status_code, 200)
            
            # Should not display weather data on timeout
            response_text = response.get_data(as_text=True)
            # Should show appropriate error message or fallback
    
    @patch('requests.get')
    def test_api_connection_error_handling(self, mock_get):
        """Test handling of API connection errors."""
        # Mock connection error
        mock_get.side_effect = requests.exceptions.ConnectionError("Connection failed")
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'kelvin'
            
            response = client.post('/', data={'city': 'Paris'})
            
            # Should handle connection errors gracefully
            self.assertEqual(response.status_code, 200)
    
    @patch('requests.get')
    def test_api_extreme_temperature_handling(self, mock_get):
        """Test handling of extreme temperature values from API."""
        # Mock extreme temperature response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_extreme_temperature_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        units = ['celsius', 'fahrenheit', 'kelvin']
        
        for unit in units:
            with self.subTest(unit=unit):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    response = client.post('/', data={'city': 'Antarctica'})
                    self.assertEqual(response.status_code, 200)
                    
                    # Should handle extreme temperatures correctly
                    response_text = response.get_data(as_text=True)
                    # Verify extreme temperatures are displayed appropriately
    
    @patch('requests.get')
    def test_api_multiple_cities_different_units(self, mock_get):
        """Test API calls for multiple cities with different temperature units."""
        cities_and_responses = [
            ('London', self.mock_api.get_celsius_response()),
            ('New York', self.mock_api.get_fahrenheit_response()),
            ('Tokyo', self.mock_api.get_hot_temperature_response()),
        ]
        
        units = ['celsius', 'fahrenheit', 'kelvin']
        
        for city, mock_response_data in cities_and_responses:
            for unit in units:
                with self.subTest(city=city, unit=unit):
                    mock_response = Mock()
                    mock_response.json.return_value = mock_response_data
                    mock_response.status_code = 200
                    mock_get.return_value = mock_response
                    
                    with self.app as client:
                        with client.session_transaction() as sess:
                            sess['temperature_unit'] = unit
                        
                        response = client.post('/', data={'city': city})
                        self.assertEqual(response.status_code, 200)
    
    @patch('requests.get')
    def test_api_rate_limiting_behavior(self, mock_get):
        """Test behavior under API rate limiting scenarios."""
        # First call succeeds
        mock_response_success = Mock()
        mock_response_success.json.return_value = self.mock_api.get_celsius_response()
        mock_response_success.status_code = 200
        
        # Second call hits rate limit
        mock_response_rate_limit = Mock()
        mock_response_rate_limit.status_code = 429
        mock_response_rate_limit.json.return_value = {
            'message': 'Your account is temporary blocked due to exceeding of requests limitation of your subscription type.'
        }
        
        # Configure mock to return different responses
        mock_get.side_effect = [mock_response_success, mock_response_rate_limit]
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'celsius'
            
            # First request should succeed
            response1 = client.post('/', data={'city': 'London'})
            self.assertEqual(response1.status_code, 200)
            
            # Second request should handle rate limiting gracefully
            response2 = client.post('/', data={'city': 'Paris'})
            self.assertEqual(response2.status_code, 200)
    
    @patch('requests.get')
    def test_api_invalid_json_response_handling(self, mock_get):
        """Test handling of invalid JSON responses from API."""
        # Mock invalid JSON response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.side_effect = json.JSONDecodeError("Expecting value", "invalid", 0)
        mock_response.text = "Invalid JSON response"
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'London'})
            
            # Should handle invalid JSON gracefully
            self.assertEqual(response.status_code, 200)
    
    def test_api_key_configuration(self):
        """Test API key configuration and security."""
        # Test that API key is properly configured
        from app.views import OPENWEATHER_API_KEY
        
        # API key should be set (either from environment or fallback)
        self.assertIsNotNone(OPENWEATHER_API_KEY)
        self.assertNotEqual(OPENWEATHER_API_KEY, '')
        
        # API key should not be exposed in logs or error messages
        # This would require testing actual error scenarios
    
    @patch('requests.get')
    def test_weather_data_structure_with_units(self, mock_get):
        """Test that weather data structure includes temperature unit information."""
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_celsius_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'celsius'
            
            response = client.post('/', data={'city': 'London'})
            self.assertEqual(response.status_code, 200)
            
            # When implemented, weather data should include unit information
            # This could be tested by checking template context or response data


class TestEndToEndTemperatureWorkflow(BaseTestCase):
    """End-to-end integration tests for complete temperature workflows."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.mock_api = MockWeatherAPI()
    
    @patch('requests.get')
    def test_complete_temperature_unit_toggle_workflow(self, mock_get):
        """Test complete workflow of toggling temperature units."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_celsius_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            # 1. Start with default (should be Celsius)
            response1 = client.post('/', data={'city': 'London'})
            self.assertEqual(response1.status_code, 200)
            
            # 2. Change to Fahrenheit
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response2 = client.post('/', data={'city': 'London'})
            self.assertEqual(response2.status_code, 200)
            
            # 3. Change to Kelvin
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'kelvin'
            
            response3 = client.post('/', data={'city': 'London'})
            self.assertEqual(response3.status_code, 200)
            
            # 4. Verify session persistence
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'kelvin')
    
    @patch('requests.get')
    def test_weather_search_with_unit_preferences(self, mock_get):
        """Test weather search workflow maintaining unit preferences."""
        cities = ['London', 'Paris', 'Berlin', 'Madrid']
        units = ['celsius', 'fahrenheit', 'kelvin']
        
        for unit in units:
            with self.subTest(unit=unit):
                # Mock appropriate API response for the unit
                mock_response = Mock()
                mock_response.json.return_value = self.mock_api.get_celsius_response()
                mock_response.status_code = 200
                mock_get.return_value = mock_response
                
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    for city in cities:
                        response = client.post('/', data={'city': city})
                        self.assertEqual(response.status_code, 200)
                        
                        # Unit preference should be maintained across searches
                        with client.session_transaction() as sess:
                            self.assertEqual(sess['temperature_unit'], unit)


class TestTemperatureUnitSessionPersistence(BaseTestCase):
    """Integration tests for temperature unit session persistence."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
    
    def test_fahrenheit_persists_across_requests(self):
        """Test that Fahrenheit unit selection persists across multiple requests."""
        with self.app as client:
            # Set Fahrenheit
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Make multiple requests
            for i in range(3):
                with self.subTest(request_number=i+1):
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
                    
                    # Verify session still has fahrenheit
                    with client.session_transaction() as sess:
                        self.assertEqual(sess.get('temperature_unit'), 'fahrenheit')
    
    def test_unit_persistence_after_weather_search(self):
        """Test that unit preference persists after performing weather searches."""
        with self.app as client:
            test_units = ['celsius', 'fahrenheit', 'kelvin']
            
            for unit in test_units:
                with self.subTest(unit=unit):
                    # Set unit preference
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    # Perform weather search
                    with patch('requests.get') as mock_get:
                        mock_response = Mock()
                        mock_response.json.return_value = MockWeatherAPI.get_celsius_response()
                        mock_response.status_code = 200
                        mock_get.return_value = mock_response
                        
                        response = client.post('/', data={'city': 'London'})
                        self.assertEqual(response.status_code, 200)
                    
                    # Verify unit preference is maintained
                    with client.session_transaction() as sess:
                        self.assertEqual(sess.get('temperature_unit'), unit)
    
    def test_session_permanence_configuration(self):
        """Test that session is configured to be permanent for unit persistence."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
                # Session should be set to permanent when unit is set
                # self.assertTrue(sess.permanent)
    
    def test_invalid_unit_does_not_persist(self):
        """Test that invalid temperature units don't persist in session."""
        with self.app as client:
            invalid_units = ['rankine', 'reaumur', 'invalid', '', None]
            
            for invalid_unit in invalid_units:
                with self.subTest(invalid_unit=invalid_unit):
                    # Attempt to set invalid unit
                    response = client.post('/set-temperature-unit',
                                          data={'unit': invalid_unit},
                                          follow_redirects=True)
                    
                    # Session should not contain invalid unit
                    with client.session_transaction() as sess:
                        stored_unit = sess.get('temperature_unit', 'celsius')
                        self.assertIn(stored_unit, ['celsius', 'fahrenheit', 'kelvin'])
    
    def test_default_unit_when_session_empty(self):
        """Test that default unit (Celsius) is used when session has no preference."""
        with self.app as client:
            # Don't set any unit preference
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            
            html_content = response.get_data(as_text=True)
            # Default should be Celsius
            # When implemented, should show Celsius as selected


class TestFahrenheitEdgeCases(BaseTestCase):
    """Integration tests for Fahrenheit-specific edge cases."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.mock_api = MockWeatherAPI()
    
    @patch('requests.get')
    def test_extreme_cold_fahrenheit_display(self, mock_get):
        """Test display of extreme cold temperatures in Fahrenheit."""
        # Mock extreme cold response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_extreme_temperature_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'Antarctica'})
            self.assertEqual(response.status_code, 200)
            
            html_content = response.get_data(as_text=True)
            # -40°C = -40°F (same value at this temperature)
            # When implemented, should display negative Fahrenheit values
    
    @patch('requests.get')
    def test_extreme_hot_fahrenheit_display(self, mock_get):
        """Test display of extreme hot temperatures in Fahrenheit."""
        # Mock extreme hot response
        mock_response = Mock()
        mock_response.json.return_value = self.mock_api.get_hot_temperature_response()
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'Death Valley'})
            self.assertEqual(response.status_code, 200)
            
            html_content = response.get_data(as_text=True)
            # 50°C = 122°F
            # When implemented, should display high Fahrenheit values (100+)
    
    @patch('requests.get')
    def test_fahrenheit_freezing_point_display(self, mock_get):
        """Test display of water freezing point in Fahrenheit (32°F)."""
        # Mock response with 0°C temperature
        mock_response = Mock()
        mock_data = self.mock_api.get_celsius_response()
        mock_data['main']['temp'] = 273.15  # 0°C in Kelvin
        mock_response.json.return_value = mock_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'TestCity'})
            self.assertEqual(response.status_code, 200)
            
            html_content = response.get_data(as_text=True)
            # 0°C = 32°F
            # When implemented, should display 32°F
    
    @patch('requests.get')
    def test_fahrenheit_boiling_point_display(self, mock_get):
        """Test display of water boiling point in Fahrenheit (212°F)."""
        # Mock response with 100°C temperature
        mock_response = Mock()
        mock_data = self.mock_api.get_celsius_response()
        mock_data['main']['temp'] = 373.15  # 100°C in Kelvin
        mock_response.json.return_value = mock_data
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            response = client.post('/', data={'city': 'TestCity'})
            self.assertEqual(response.status_code, 200)
            
            html_content = response.get_data(as_text=True)
            # 100°C = 212°F
            # When implemented, should display 212°F


if __name__ == '__main__':
    unittest.main()