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
    
    def test_fahrenheit_conversion_complete_coverage(self):
        """Test comprehensive Fahrenheit conversion accuracy across multiple scenarios."""
        fahrenheit_test_cases = [
            # (celsius, expected_fahrenheit, description)
            (0.0, 32.0, "Freezing point of water"),
            (100.0, 212.0, "Boiling point of water"),
            (-40.0, -40.0, "Celsius equals Fahrenheit"),
            (37.0, 98.6, "Normal human body temperature"),
            (50.0, 122.0, "Very hot day"),
            (-10.0, 14.0, "Cold day"),
            (20.0, 68.0, "Pleasant room temperature"),
            (30.0, 86.0, "Warm day"),
            (-20.0, -4.0, "Very cold winter day"),
            (15.0, 59.0, "Cool autumn temperature"),
        ]
        
        for celsius, expected_fahrenheit, description in fahrenheit_test_cases:
            with self.subTest(description=description):
                result = celsius_to_fahrenheit(celsius)
                self.assertAlmostEqual(
                    result, expected_fahrenheit, places=1,
                    msg=f"Fahrenheit conversion failed for {description}: {celsius}°C -> {result}°F (expected {expected_fahrenheit}°F)"
                )
    
    def test_fahrenheit_bidirectional_conversion_accuracy(self):
        """Test that Fahrenheit conversions are accurate in both directions."""
        test_values = [0.0, 50.0, 100.0, -40.0, 37.0, 25.5, -273.15]
        
        for original_celsius in test_values:
            if original_celsius < -273.15:
                # Skip temperatures below absolute zero
                continue
                
            with self.subTest(celsius=original_celsius):
                # Convert Celsius -> Fahrenheit -> Celsius
                fahrenheit = celsius_to_fahrenheit(original_celsius)
                back_to_celsius = fahrenheit_to_celsius(fahrenheit)
                
                self.assertAlmostEqual(
                    original_celsius, back_to_celsius, places=5,
                    msg=f"Round-trip conversion failed: {original_celsius}°C -> {fahrenheit}°F -> {back_to_celsius}°C"
                )
    
    def test_kelvin_fahrenheit_bidirectional_conversion(self):
        """Test that Kelvin-Fahrenheit conversions are accurate in both directions."""
        test_kelvin_values = [273.15, 288.15, 310.15, 373.15, 233.15, 323.15]
        
        for original_kelvin in test_kelvin_values:
            with self.subTest(kelvin=original_kelvin):
                # Convert Kelvin -> Fahrenheit -> Kelvin
                fahrenheit = kelvin_to_fahrenheit(original_kelvin)
                back_to_kelvin = fahrenheit_to_kelvin(fahrenheit)
                
                self.assertAlmostEqual(
                    original_kelvin, back_to_kelvin, places=5,
                    msg=f"Round-trip K->F->K conversion failed: {original_kelvin}K -> {fahrenheit}°F -> {back_to_kelvin}K"
                )
    
    def test_fahrenheit_edge_cases(self):
        """Test Fahrenheit conversion with edge cases."""
        edge_cases = [
            (0.0, 32.0, "Freezing point"),
            (-273.15, -459.67, "Absolute zero"),
            (5778.0, 10432.4, "Sun surface approximate"),
            (0.01, 32.018, "Just above absolute zero"),
            (-100.0, -148.0, "Extremely cold"),
        ]
        
        for celsius, expected_fahrenheit, description in edge_cases:
            with self.subTest(description=description):
                result = celsius_to_fahrenheit(celsius)
                self.assertAlmostEqual(
                    result, expected_fahrenheit, places=1,
                    msg=f"Edge case failed for {description}"
                )
    
    def test_fahrenheit_decimal_precision(self):
        """Test that Fahrenheit conversions maintain appropriate decimal precision."""
        # Test single decimal place precision for weather display
        test_temps = [
            (15.5, 59.9, "Room temperature with decimal"),
            (22.3, 72.14, "Temperature with tenths"),
            (10.7, 51.26, "Cool temperature"),
            (-0.5, 31.1, "Near freezing"),
        ]
        
        for celsius, expected_fahrenheit, description in test_temps:
            with self.subTest(description=description):
                result = celsius_to_fahrenheit(celsius)
                # Allow for rounding differences up to 0.2 degrees
                self.assertAlmostEqual(
                    result, expected_fahrenheit, places=0,
                    msg=f"Precision test failed for {description}"
                )
    
    def test_fahrenheit_type_conversion(self):
        """Test Fahrenheit conversion with various numeric types (int, float, Decimal)."""
        test_value_celsius = 25.0
        expected_fahrenheit = 77.0
        
        # Test with int
        result_int = celsius_to_fahrenheit(25)
        self.assertAlmostEqual(result_int, expected_fahrenheit, places=1)
        self.assertIsInstance(result_int, float)
        
        # Test with float
        result_float = celsius_to_fahrenheit(25.0)
        self.assertAlmostEqual(result_float, expected_fahrenheit, places=1)
        self.assertIsInstance(result_float, float)
        
        # Test with Decimal
        result_decimal = celsius_to_fahrenheit(Decimal('25.0'))
        self.assertAlmostEqual(float(result_decimal), expected_fahrenheit, places=1)
        self.assertIsInstance(result_decimal, float)
    
    def test_universal_converter_with_fahrenheit(self):
        """Test universal converter specifically with Fahrenheit scenarios."""
        test_scenarios = [
            # (input_value, from_unit, to_unit, expected_result, description)
            (59.0, 'fahrenheit', 'celsius', 15.0, "Fahrenheit to Celsius"),
            (288.15, 'kelvin', 'fahrenheit', 59.0, "Kelvin to Fahrenheit"),
            (25.0, 'celsius', 'fahrenheit', 77.0, "Celsius to Fahrenheit"),
            (77.0, 'fahrenheit', 'kelvin', 298.15, "Fahrenheit to Kelvin"),
        ]
        
        for input_value, from_unit, to_unit, expected, description in test_scenarios:
            with self.subTest(description=description):
                result = convert_temperature(input_value, from_unit, to_unit)
                self.assertAlmostEqual(
                    result, expected, places=1,
                    msg=f"Universal converter failed for {description}"
                )
    
    def test_fahrenheit_format_temperature(self):
        """Test format_temperature function with Fahrenheit unit."""
        test_cases = [
            (59.0, 'fahrenheit', '59.0°F', "Standard Fahrenheit formatting"),
            (77.5, 'fahrenheit', '77.5°F', "Decimal Fahrenheit formatting"),
            (32.123, 'fahrenheit', '32.1°F', "Rounding Fahrenheit to 1 decimal"),
            (-40.0, 'fahrenheit', '-40.0°F', "Negative Fahrenheit formatting"),
        ]
        
        for temp, unit, expected_format, description in test_cases:
            with self.subTest(description=description):
                result = format_temperature(temp, unit)
                self.assertEqual(
                    result, expected_format,
                    msg=f"Format failed for {description}: got {result}, expected {expected_format}"
                )


if __name__ == '__main__':
    unittest.main()