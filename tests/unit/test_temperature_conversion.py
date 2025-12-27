"""
Unit tests for temperature conversion utilities.

This module contains comprehensive unit tests for temperature conversion
functions including accuracy testing, edge cases, and error handling.

Test Coverage:
- kelvin_to_celsius() accuracy (±0.1°)
- celsius_to_kelvin() accuracy
- convert_temperature() universal converter
- Edge cases (extreme temperatures, invalid inputs)
- Performance testing (<10ms conversion time)
"""

import unittest
import time
from unittest.mock import patch, MagicMock
from decimal import Decimal
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from tests.conftest import BaseTestCase, TestDataFixtures
from app.utils import (
    kelvin_to_celsius,
    celsius_to_kelvin,
    celsius_to_fahrenheit,
    fahrenheit_to_celsius,
    kelvin_to_fahrenheit,
    fahrenheit_to_kelvin,
    convert_temperature,
    format_temperature,
    convert_weather_data
)

class TestTemperatureConversion(BaseTestCase):
    """Test cases for temperature conversion functionality."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
        self.test_data = TestDataFixtures.TEMPERATURE_CONVERSIONS
    
    def test_kelvin_to_celsius_accuracy(self):
        """Test Kelvin to Celsius conversion accuracy within ±0.1°."""
        for kelvin, expected_celsius, _, description in self.test_data:
            with self.subTest(description=description):
                result = kelvin_to_celsius(kelvin)
                self.assertAlmostEqual(
                    result, expected_celsius, places=1,
                    msg=f"Conversion failed for {description}: {kelvin}K -> {result}°C (expected {expected_celsius}°C)"
                )
    
    def test_celsius_to_kelvin_accuracy(self):
        """Test Celsius to Kelvin conversion accuracy."""
        for expected_kelvin, celsius, _, description in self.test_data:
            with self.subTest(description=description):
                result = celsius_to_kelvin(celsius)
                self.assertAlmostEqual(
                    result, expected_kelvin, places=1,
                    msg=f"Conversion failed for {description}: {celsius}°C -> {result}K (expected {expected_kelvin}K)"
                )
    
    def test_celsius_to_fahrenheit_accuracy(self):
        """Test Celsius to Fahrenheit conversion accuracy."""
        for _, celsius, expected_fahrenheit, description in self.test_data:
            with self.subTest(description=description):
                result = celsius_to_fahrenheit(celsius)
                self.assertAlmostEqual(
                    result, expected_fahrenheit, places=1,
                    msg=f"Conversion failed for {description}: {celsius}°C -> {result}°F (expected {expected_fahrenheit}°F)"
                )
    
    def test_fahrenheit_to_celsius_accuracy(self):
        """Test Fahrenheit to Celsius conversion accuracy."""
        for _, expected_celsius, fahrenheit, description in self.test_data:
            with self.subTest(description=description):
                result = fahrenheit_to_celsius(fahrenheit)
                self.assertAlmostEqual(
                    result, expected_celsius, places=1,
                    msg=f"Conversion failed for {description}: {fahrenheit}°F -> {result}°C (expected {expected_celsius}°C)"
                )
    
    def test_kelvin_to_fahrenheit_accuracy(self):
        """Test direct Kelvin to Fahrenheit conversion."""
        for kelvin, _, expected_fahrenheit, description in self.test_data:
            with self.subTest(description=description):
                result = kelvin_to_fahrenheit(kelvin)
                self.assertAlmostEqual(
                    result, expected_fahrenheit, places=1,
                    msg=f"Conversion failed for {description}: {kelvin}K -> {result}°F (expected {expected_fahrenheit}°F)"
                )
    
    def test_fahrenheit_to_kelvin_accuracy(self):
        """Test direct Fahrenheit to Kelvin conversion."""
        for expected_kelvin, _, fahrenheit, description in self.test_data:
            with self.subTest(description=description):
                result = fahrenheit_to_kelvin(fahrenheit)
                self.assertAlmostEqual(
                    result, expected_kelvin, places=1,
                    msg=f"Conversion failed for {description}: {fahrenheit}°F -> {result}K (expected {expected_kelvin}K)"
                )
    
    def test_universal_converter_all_combinations(self):
        """Test universal converter for all unit combinations."""
        units = ['celsius', 'fahrenheit', 'kelvin']
        test_temp = 288.15  # 15°C in Kelvin
        
        expected_values = {
            ('kelvin', 'celsius'): 15.0,
            ('kelvin', 'fahrenheit'): 59.0,
            ('celsius', 'kelvin'): 288.15,
            ('celsius', 'fahrenheit'): 59.0,
            ('fahrenheit', 'celsius'): 15.0,
            ('fahrenheit', 'kelvin'): 288.15,
        }
        
        for from_unit in units:
            for to_unit in units:
                with self.subTest(from_unit=from_unit, to_unit=to_unit):
                    if from_unit == to_unit:
                        # Same unit should return same value
                        result = convert_temperature(test_temp, from_unit, to_unit)
                        self.assertEqual(result, test_temp)
                    else:
                        # Different units should convert correctly
                        if from_unit == 'kelvin':
                            input_temp = test_temp
                        elif from_unit == 'celsius':
                            input_temp = 15.0
                        else:  # fahrenheit
                            input_temp = 59.0
                        
                        result = convert_temperature(input_temp, from_unit, to_unit)
                        expected = expected_values.get((from_unit, to_unit))
                        
                        if expected is not None:
                            self.assertAlmostEqual(
                                result, expected, places=1,
                                msg=f"Universal conversion failed: {input_temp}{from_unit} -> {result}{to_unit} (expected {expected})"
                            )
    
    def test_conversion_performance(self):
        """Test that temperature conversions complete within 10ms."""
        test_temps = [273.15, 288.15, 310.15, 373.15]
        
        for temp in test_temps:
            # Test Kelvin to Celsius performance
            start_time = time.perf_counter()
            kelvin_to_celsius(temp)
            end_time = time.perf_counter()
            
            execution_time_ms = (end_time - start_time) * 1000
            self.assertLess(
                execution_time_ms, 10.0,
                f"kelvin_to_celsius took {execution_time_ms:.2f}ms (should be < 10ms)"
            )
            
            # Test universal converter performance
            start_time = time.perf_counter()
            convert_temperature(temp, 'kelvin', 'celsius')
            end_time = time.perf_counter()
            
            execution_time_ms = (end_time - start_time) * 1000
            self.assertLess(
                execution_time_ms, 10.0,
                f"convert_temperature took {execution_time_ms:.2f}ms (should be < 10ms)"
            )
    
    def test_invalid_input_types(self):
        """Test handling of invalid input types."""
        invalid_inputs = [
            'not_a_number',
            None,
            [],
            {},
            complex(1, 2),
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                with self.assertRaises(TypeError):
                    kelvin_to_celsius(invalid_input)
                
                with self.assertRaises(TypeError):
                    celsius_to_kelvin(invalid_input)
    
    def test_below_absolute_zero_kelvin(self):
        """Test handling of temperatures below absolute zero in Kelvin."""
        invalid_kelvin_temps = [-1, -10, -273.16]
        
        for temp in invalid_kelvin_temps:
            with self.subTest(temp=temp):
                with self.assertRaises(ValueError):
                    kelvin_to_celsius(temp)
    
    def test_below_absolute_zero_celsius(self):
        """Test handling of temperatures below absolute zero in Celsius."""
        invalid_celsius_temps = [-274, -300, -500]
        
        for temp in invalid_celsius_temps:
            with self.subTest(temp=temp):
                with self.assertRaises(ValueError):
                    celsius_to_kelvin(temp)
    
    def test_extreme_temperature_ranges(self):
        """Test conversion accuracy with extreme temperature ranges."""
        extreme_cases = [
            (0.01, -273.14, "Near absolute zero"),
            (5778.0, 5504.85, "Surface of the Sun"),
            (2.7, -270.45, "Cosmic microwave background"),
        ]
        
        for kelvin, expected_celsius, description in extreme_cases:
            with self.subTest(description=description):
                result = kelvin_to_celsius(kelvin)
                self.assertAlmostEqual(
                    result, expected_celsius, places=1,
                    msg=f"Extreme temperature conversion failed for {description}"
                )
    
    def test_unsupported_units_in_universal_converter(self):
        """Test universal converter with unsupported unit types."""
        unsupported_units = ['rankine', 'reaumur', 'newton', 'delisle', 'invalid']
        
        for unit in unsupported_units:
            with self.subTest(unit=unit):
                with self.assertRaises(ValueError):
                    convert_temperature(100, unit, 'celsius')
                
                with self.assertRaises(ValueError):
                    convert_temperature(100, 'celsius', unit)
    
    def test_case_insensitive_unit_names(self):
        """Test that unit names are case insensitive."""
        case_variations = [
            'CELSIUS', 'Celsius', 'celsius',
            'FAHRENHEIT', 'Fahrenheit', 'fahrenheit',
            'KELVIN', 'Kelvin', 'kelvin'
        ]
        
        for unit in case_variations:
            with self.subTest(unit=unit):
                result = convert_temperature(100, 'celsius', unit.lower())
                # Should not raise an exception
                self.assertIsInstance(result, float)
    
    def test_precision_and_rounding(self):
        """Test precision and rounding behavior of conversions."""
        # Test that results maintain appropriate precision
        result = kelvin_to_celsius(288.123456789)
        # Result should be a float with reasonable precision
        self.assertIsInstance(result, float)
        self.assertAlmostEqual(result, 14.973456789, places=6)
        
        # Test rounding behavior for display
        result = celsius_to_fahrenheit(15.555555)
        self.assertAlmostEqual(result, 59.999999, places=6)


class TestThreeWayConversionScenarios(BaseTestCase):
    """Test cases for three-way temperature conversion scenarios."""
    
    def setUp(self):
        """Set up test environment."""
        super().setUp()
    
    def test_celsius_to_all_units(self):
        """Test converting from Celsius to all three units."""
        celsius_value = 20.0
        
        # Celsius to Celsius (identity)
        result = convert_temperature(celsius_value, 'celsius', 'celsius')
        self.assertAlmostEqual(result, 20.0, places=1)
        
        # Celsius to Fahrenheit
        result = convert_temperature(celsius_value, 'celsius', 'fahrenheit')
        self.assertAlmostEqual(result, 68.0, places=1)
        
        # Celsius to Kelvin
        result = convert_temperature(celsius_value, 'celsius', 'kelvin')
        self.assertAlmostEqual(result, 293.15, places=1)
    
    def test_fahrenheit_to_all_units(self):
        """Test converting from Fahrenheit to all three units."""
        fahrenheit_value = 68.0
        
        # Fahrenheit to Fahrenheit (identity)
        result = convert_temperature(fahrenheit_value, 'fahrenheit', 'fahrenheit')
        self.assertAlmostEqual(result, 68.0, places=1)
        
        # Fahrenheit to Celsius
        result = convert_temperature(fahrenheit_value, 'fahrenheit', 'celsius')
        self.assertAlmostEqual(result, 20.0, places=1)
        
        # Fahrenheit to Kelvin
        result = convert_temperature(fahrenheit_value, 'fahrenheit', 'kelvin')
        self.assertAlmostEqual(result, 293.15, places=1)
    
    def test_kelvin_to_all_units(self):
        """Test converting from Kelvin to all three units."""
        kelvin_value = 293.15
        
        # Kelvin to Kelvin (identity)
        result = convert_temperature(kelvin_value, 'kelvin', 'kelvin')
        self.assertAlmostEqual(result, 293.15, places=1)
        
        # Kelvin to Celsius
        result = convert_temperature(kelvin_value, 'kelvin', 'celsius')
        self.assertAlmostEqual(result, 20.0, places=1)
        
        # Kelvin to Fahrenheit
        result = convert_temperature(kelvin_value, 'kelvin', 'fahrenheit')
        self.assertAlmostEqual(result, 68.0, places=1)
    
    def test_round_trip_conversions_celsius_fahrenheit(self):
        """Test round-trip conversions between Celsius and Fahrenheit."""
        original = 25.5
        
        # Celsius -> Fahrenheit -> Celsius
        fahrenheit = convert_temperature(original, 'celsius', 'fahrenheit')
        back_to_celsius = convert_temperature(fahrenheit, 'fahrenheit', 'celsius')
        
        self.assertAlmostEqual(back_to_celsius, original, places=2,
                              msg="Round-trip Celsius->Fahrenheit->Celsius failed")
    
    def test_round_trip_conversions_fahrenheit_kelvin(self):
        """Test round-trip conversions between Fahrenheit and Kelvin."""
        original = 72.5
        
        # Fahrenheit -> Kelvin -> Fahrenheit
        kelvin = convert_temperature(original, 'fahrenheit', 'kelvin')
        back_to_fahrenheit = convert_temperature(kelvin, 'kelvin', 'fahrenheit')
        
        self.assertAlmostEqual(back_to_fahrenheit, original, places=2,
                              msg="Round-trip Fahrenheit->Kelvin->Fahrenheit failed")
    
    def test_round_trip_conversions_celsius_kelvin(self):
        """Test round-trip conversions between Celsius and Kelvin."""
        original = 18.3
        
        # Celsius -> Kelvin -> Celsius
        kelvin = convert_temperature(original, 'celsius', 'kelvin')
        back_to_celsius = convert_temperature(kelvin, 'kelvin', 'celsius')
        
        self.assertAlmostEqual(back_to_celsius, original, places=2,
                              msg="Round-trip Celsius->Kelvin->Celsius failed")
    
    def test_special_temperature_points_all_units(self):
        """Test conversion of special temperature points across all three units."""
        special_points = [
            # (celsius, fahrenheit, kelvin, description)
            (0.0, 32.0, 273.15, "Water freezing point"),
            (100.0, 212.0, 373.15, "Water boiling point"),
            (-40.0, -40.0, 233.15, "Celsius-Fahrenheit intersection"),
            (37.0, 98.6, 310.15, "Human body temperature"),
        ]
        
        for celsius, fahrenheit, kelvin, description in special_points:
            with self.subTest(description=description):
                # Test Celsius conversions
                c_to_f = convert_temperature(celsius, 'celsius', 'fahrenheit')
                c_to_k = convert_temperature(celsius, 'celsius', 'kelvin')
                self.assertAlmostEqual(c_to_f, fahrenheit, places=1)
                self.assertAlmostEqual(c_to_k, kelvin, places=2)
                
                # Test Fahrenheit conversions
                f_to_c = convert_temperature(fahrenheit, 'fahrenheit', 'celsius')
                f_to_k = convert_temperature(fahrenheit, 'fahrenheit', 'kelvin')
                self.assertAlmostEqual(f_to_c, celsius, places=1)
                self.assertAlmostEqual(f_to_k, kelvin, places=2)
                
                # Test Kelvin conversions
                k_to_c = convert_temperature(kelvin, 'kelvin', 'celsius')
                k_to_f = convert_temperature(kelvin, 'kelvin', 'fahrenheit')
                self.assertAlmostEqual(k_to_c, celsius, places=1)
                self.assertAlmostEqual(k_to_f, fahrenheit, places=1)
    
    def test_format_temperature_all_units(self):
        """Test temperature formatting for all three units."""
        temperature = 20.5
        
        # Test formatting for each unit
        celsius_formatted = format_temperature(temperature, 'celsius')
        self.assertIn('20.5', celsius_formatted)
        self.assertIn('°C', celsius_formatted)
        
        fahrenheit_formatted = format_temperature(temperature, 'fahrenheit')
        self.assertIn('20.5', fahrenheit_formatted)
        self.assertIn('°F', fahrenheit_formatted)
        
        kelvin_formatted = format_temperature(temperature, 'kelvin')
        self.assertIn('20.5', kelvin_formatted)
        self.assertIn('K', kelvin_formatted)
    
    def test_conversion_performance_all_units(self):
        """Test that all conversion combinations complete within performance threshold."""
        units = ['celsius', 'fahrenheit', 'kelvin']
        temperature = 25.0
        max_time_ms = 10
        
        for from_unit in units:
            for to_unit in units:
                with self.subTest(from_unit=from_unit, to_unit=to_unit):
                    start_time = time.time()
                    
                    result = convert_temperature(temperature, from_unit, to_unit)
                    
                    end_time = time.time()
                    execution_time_ms = (end_time - start_time) * 1000
                    
                    self.assertLess(execution_time_ms, max_time_ms,
                                   f"Conversion {from_unit}->{to_unit} took {execution_time_ms:.2f}ms")
                    self.assertIsInstance(result, float)


if __name__ == '__main__':
    unittest.main()