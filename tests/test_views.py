from flask import Flask
import unittest
from app import app  # import the Flask app from your application module

class TestViews(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    def test_index_post(self):
        cities = ['London', 'Paris', 'New York', 'Tokyo', 'Sydney']
        for city in cities:
            response = self.app.post('/', data={'city': city})
            self.assertEqual(response.status_code, 200)
            self.assertIn(bytes(city, 'utf-8'), response.data)

    # Test to verify temperature is displayed in Celsius
    def test_temperature_display_in_celsius(self):
        response = self.app.get('/')
        self.assertIn(b'Temperature: ', response.data)
        self.assertIn(b'°C', response.data)
