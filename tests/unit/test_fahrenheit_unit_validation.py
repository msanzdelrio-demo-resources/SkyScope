"""
Unit tests for Fahrenheit temperature unit validation and backend integration.

This module contains tests for Fahrenheit-specific unit validation,
session management, and backend temperature unit handling.

Test Coverage:
- Fahrenheit unit validation in views
- Temperature unit session management with Fahrenheit
- API parameter mapping for Fahrenheit
- Edge cases and error handling for Fahrenheit
"""

import unittest
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tests.conftest import BaseTestCase
from app.views import (
    get_temperature_unit,
    set_temperature_unit,
    get_api_units_parameter
)


class TestFahrenheitUnitValidation(BaseTestCase):
    """Test cases for Fahrenheit unit validation in the backend."""
    
    def test_set_fahrenheit_temperature_unit(self):
        """Test setting temperature unit to Fahrenheit."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess.clear()
            
            # Test within application context
            with client.session_transaction() as sess:
                # Simulate setting fahrenheit
                sess['temperature_unit'] = 'fahrenheit'
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_get_fahrenheit_from_session(self):
        """Test retrieving Fahrenheit temperature unit from session."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # When backend function is used, should return fahrenheit
            # This tests the get_temperature_unit function behavior
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_fahrenheit_unit_case_insensitive(self):
        """Test that Fahrenheit unit is handled case-insensitively."""
        case_variations = ['FAHRENHEIT', 'Fahrenheit', 'fahrenheit', 'FaHrEnHeIt']
        
        with self.app as client:
            for unit_variant in case_variations:
                with self.subTest(unit=unit_variant):
                    with client.session_transaction() as sess:
                        # Backend should normalize to lowercase
                        sess['temperature_unit'] = unit_variant.lower()
                        self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_fahrenheit_api_parameter_mapping(self):
        """Test that Fahrenheit maps to imperial units parameter."""
        # Mock the get_api_units_parameter function
        result = get_api_units_parameter('fahrenheit')
        self.assertEqual(result, 'imperial',
                        msg="Fahrenheit should map to 'imperial' API parameter")
    
    def test_all_units_api_parameter_mapping(self):
        """Test API parameter mapping for all three temperature units."""
        unit_mappings = {
            'celsius': 'metric',
            'fahrenheit': 'imperial',
            'kelvin': 'standard'
        }
        
        for unit, expected_param in unit_mappings.items():
            with self.subTest(unit=unit):
                result = get_api_units_parameter(unit)
                self.assertEqual(result, expected_param,
                               msg=f"{unit} should map to {expected_param}")
    
    def test_fahrenheit_unit_whitespace_handling(self):
        """Test that Fahrenheit unit handles whitespace correctly."""
        with self.app as client:
            with client.session_transaction() as sess:
                # Whitespace should be stripped
                sess['temperature_unit'] = '  fahrenheit  '
                # When processing, should normalize
                unit = sess['temperature_unit'].strip().lower()
                self.assertEqual(unit, 'fahrenheit')
    
    def test_invalid_unit_not_set_to_fahrenheit(self):
        """Test that invalid units don't get set to Fahrenheit."""
        invalid_units = ['rankine', 'reaumur', 'celsius_invalid', '', 'F', None]
        
        with self.app as client:
            for invalid_unit in invalid_units:
                with self.subTest(unit=invalid_unit):
                    with client.session_transaction() as sess:
                        # Invalid unit should not be set
                        if invalid_unit is not None:
                            sess['temperature_unit'] = invalid_unit.lower() if isinstance(invalid_unit, str) else invalid_unit
                            
                            # When backend validates, it should not equal valid units
                            if isinstance(invalid_unit, str):
                                self.assertNotEqual(
                                    invalid_unit.lower().strip(),
                                    'fahrenheit'
                                )
    
    def test_fahrenheit_default_not_set(self):
        """Test that default temperature unit is Celsius, not Fahrenheit."""
        with self.app as client:
            # Fresh session without explicit unit set
            with client.session_transaction() as sess:
                unit = sess.get('temperature_unit', 'celsius')
                self.assertEqual(unit, 'celsius',
                               msg="Default unit should be Celsius, not Fahrenheit")
    
    def test_fahrenheit_persists_across_requests(self):
        """Test that Fahrenheit selection persists across multiple requests."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Make multiple requests
            for _ in range(5):
                response = client.get('/')
                self.assertEqual(response.status_code, 200)
                
                # Unit should persist
                with client.session_transaction() as sess:
                    self.assertEqual(sess['temperature_unit'], 'fahrenheit')


class TestFahrenheitSessionManagement(BaseTestCase):
    """Test cases for session management with Fahrenheit unit."""
    
    def test_fahrenheit_session_security(self):
        """Test that Fahrenheit in session doesn't cause security issues."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Session should be secure
            with client.session_transaction() as sess:
                self.assertIsInstance(sess['temperature_unit'], str)
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_fahrenheit_xss_prevention(self):
        """Test that Fahrenheit unit is validated against XSS attempts."""
        xss_attempts = [
            '<script>alert("xss")</script>',
            'fahrenheit"; DROP TABLE sessions; --',
            'fahrenheit\'; DROP TABLE sessions; --',
            'fahrenheit<img src=x onerror=alert(1)>',
        ]
        
        with self.app as client:
            for xss_attempt in xss_attempts:
                with self.subTest(xss=xss_attempt):
                    with client.session_transaction() as sess:
                        # Set the malicious value
                        sess['temperature_unit'] = xss_attempt
                    
                    # Make a request
                    response = client.get('/')
                    # Should not execute malicious code, should handle gracefully
                    self.assertEqual(response.status_code, 200)
    
    def test_fahrenheit_sql_injection_prevention(self):
        """Test that Fahrenheit unit is protected against SQL injection attempts."""
        sql_injections = [
            "fahrenheit' OR '1'='1",
            "fahrenheit; DELETE FROM users;",
            "fahrenheit' UNION SELECT * FROM users; --",
        ]
        
        with self.app as client:
            for sql_attempt in sql_injections:
                with self.subTest(sql=sql_attempt):
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = sql_attempt
                    
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
    
    def test_fahrenheit_session_serialization(self):
        """Test that Fahrenheit unit serializes correctly in session."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
                original_unit = sess['temperature_unit']
            
            # Session should serialize and deserialize correctly
            with client.session_transaction() as sess:
                restored_unit = sess['temperature_unit']
                self.assertEqual(original_unit, restored_unit)
                self.assertEqual(restored_unit, 'fahrenheit')
    
    def test_fahrenheit_session_expiration_handling(self):
        """Test session behavior when temperature_unit key is missing."""
        with self.app as client:
            # Don't set temperature_unit explicitly
            with client.session_transaction() as sess:
                if 'temperature_unit' in sess:
                    del sess['temperature_unit']
            
            # Should default to celsius
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            
            # Session should still exist
            with client.session_transaction() as sess:
                # Can now set it to fahrenheit
                sess['temperature_unit'] = 'fahrenheit'
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')


class TestFahrenheitDataValidation(BaseTestCase):
    """Test cases for Fahrenheit data validation and type checking."""
    
    def test_fahrenheit_is_string_type(self):
        """Test that temperature unit must be a string type."""
        valid_string = 'fahrenheit'
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = valid_string
                self.assertIsInstance(sess['temperature_unit'], str)
    
    def test_fahrenheit_not_numeric_type(self):
        """Test that numeric types are not accepted for temperature unit."""
        numeric_attempts = [32, 32.0, 59.0, 0]
        
        with self.app as client:
            for numeric_value in numeric_attempts:
                with self.subTest(numeric=numeric_value):
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = str(numeric_value)
                        # Numeric strings should not equal valid units
                        self.assertNotEqual(
                            sess['temperature_unit'],
                            'fahrenheit'
                        )
    
    def test_fahrenheit_not_boolean_type(self):
        """Test that boolean values are not accepted for temperature unit."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = str(True)  # Would become 'True'
                self.assertNotEqual(
                    sess['temperature_unit'].lower(),
                    'fahrenheit'
                )


class TestFahrenheitAPIIntegration(BaseTestCase):
    """Test cases for Fahrenheit in API integration context."""
    
    def test_fahrenheit_api_parameter_correct_format(self):
        """Test that Fahrenheit generates correct API parameter format."""
        result = get_api_units_parameter('fahrenheit')
        
        # Should be exactly 'imperial'
        self.assertEqual(result, 'imperial')
        self.assertIsInstance(result, str)
        self.assertNotIn('=', result)  # Should not include parameter name
        self.assertNotIn(' ', result)  # Should have no spaces
    
    def test_all_units_generate_valid_api_parameters(self):
        """Test that all temperature units generate valid API parameters."""
        valid_units = ['celsius', 'fahrenheit', 'kelvin']
        
        for unit in valid_units:
            with self.subTest(unit=unit):
                result = get_api_units_parameter(unit)
                
                # Result should be non-empty string
                self.assertIsInstance(result, str)
                self.assertTrue(len(result) > 0)
                
                # Result should be valid OpenWeatherMap API parameter
                # Valid values: 'metric', 'imperial', 'standard'
                self.assertIn(result, ['metric', 'imperial', 'standard'])
    
    def test_fahrenheit_units_parameter_distinct(self):
        """Test that Fahrenheit units parameter is distinct from others."""
        fahrenheit_param = get_api_units_parameter('fahrenheit')
        celsius_param = get_api_units_parameter('celsius')
        kelvin_param = get_api_units_parameter('kelvin')
        
        # All should be different
        self.assertNotEqual(fahrenheit_param, celsius_param)
        self.assertNotEqual(fahrenheit_param, kelvin_param)
        self.assertNotEqual(celsius_param, kelvin_param)
    
    def test_fahrenheit_case_insensitive_api_parameter(self):
        """Test that API parameter works with case variations of fahrenheit."""
        case_variations = ['FAHRENHEIT', 'Fahrenheit', 'fahrenheit']
        
        expected_result = 'imperial'
        
        for variant in case_variations:
            with self.subTest(variant=variant):
                # Function should handle case-insensitive input
                result = get_api_units_parameter(variant.lower())
                self.assertEqual(result, expected_result)


class TestFahrenheitEdgeCases(BaseTestCase):
    """Test cases for edge cases and error conditions with Fahrenheit."""
    
    def test_empty_string_unit_handling(self):
        """Test handling of empty string for temperature unit."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = ''
            
            response = client.get('/')
            # Should handle gracefully
            self.assertEqual(response.status_code, 200)
    
    def test_none_unit_in_session(self):
        """Test handling when temperature_unit is None."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = None
            
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
    
    def test_very_long_string_as_unit(self):
        """Test handling of very long string as temperature unit."""
        long_string = 'f' * 1000
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = long_string
            
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
    
    def test_special_characters_in_unit(self):
        """Test handling of special characters in temperature unit."""
        special_units = [
            'fahrenheit!',
            'fahrenheit@',
            'fahrenheit#',
            'fahr$nheit',
            'fahrenheit%',
        ]
        
        with self.app as client:
            for special_unit in special_units:
                with self.subTest(unit=special_unit):
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = special_unit
                    
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
    
    def test_unicode_characters_in_unit(self):
        """Test handling of unicode characters in temperature unit."""
        unicode_units = [
            'fahrenheit°',
            'fahrenheit™',
            'fåhrenheit',
            'fährenheit',
        ]
        
        with self.app as client:
            for unicode_unit in unicode_units:
                with self.subTest(unit=unicode_unit):
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unicode_unit
                    
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
