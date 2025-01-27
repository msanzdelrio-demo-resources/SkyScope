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
            self.assertIn(b'Wind Speed:', response.data)
            self.assertIn(b'Rain:', response.data)
            self.assertIn(b'Pressure:', response.data)
            self.assertIn(b'Visibility:', response.data)
            self.assertIn(b'Snow:', response.data)

    def test_weather_info(self):
        response = self.app.post('/', data={'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Weather in London', response.data)
        self.assertIn(b'Temperature:', response.data)
        self.assertIn(b'Wind Speed:', response.data)
        self.assertIn(b'Rain:', response.data)
        self.assertIn(b'Pressure:', response.data)
        self.assertIn(b'Visibility:', response.data)
        self.assertIn(b'Snow:', response.data)

    def test_temperature_in_celsius(self):
        response = self.app.post('/', data={'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Temperature:', response.data)
        self.assertRegex(response.data.decode('utf-8'), r'Temperature: \d+\.\d+ °C')

    def test_visibility_field(self):
        response = self.app.post('/', data={'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Visibility:', response.data)

    def test_snow_field(self):
        response = self.app.post('/', data={'city': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Snow:', response.data)
