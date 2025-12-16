"""
Temperature conversion utilities for SkyScope application.

This module provides accurate temperature conversion functions
with comprehensive error handling and validation.
"""

from decimal import Decimal
from typing import Union, Dict, Any


def kelvin_to_celsius(kelvin_temp: Union[int, float, Decimal]) -> float:
    """
    Convert temperature from Kelvin to Celsius.
    
    Args:
        kelvin_temp: Temperature in Kelvin
        
    Returns:
        Temperature in Celsius
        
    Raises:
        ValueError: If temperature is below absolute zero
        TypeError: If input is not a number
    """
    if not isinstance(kelvin_temp, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    if kelvin_temp < 0:
        raise ValueError("Temperature cannot be below absolute zero")
        
    return float(kelvin_temp) - 273.15


def celsius_to_kelvin(celsius_temp: Union[int, float, Decimal]) -> float:
    """
    Convert temperature from Celsius to Kelvin.
    
    Args:
        celsius_temp: Temperature in Celsius
        
    Returns:
        Temperature in Kelvin
        
    Raises:
        ValueError: If temperature is below absolute zero in Celsius (-273.15°C)
        TypeError: If input is not a number
    """
    if not isinstance(celsius_temp, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    if celsius_temp < -273.15:
        raise ValueError("Temperature cannot be below absolute zero (-273.15°C)")
    
    return float(celsius_temp) + 273.15


def celsius_to_fahrenheit(celsius_temp: Union[int, float, Decimal]) -> float:
    """
    Convert temperature from Celsius to Fahrenheit.
    
    Args:
        celsius_temp: Temperature in Celsius
        
    Returns:
        Temperature in Fahrenheit
        
    Raises:
        TypeError: If input is not a number
    """
    if not isinstance(celsius_temp, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    return float(celsius_temp) * 9/5 + 32


def fahrenheit_to_celsius(fahrenheit_temp: Union[int, float, Decimal]) -> float:
    """
    Convert temperature from Fahrenheit to Celsius.
    
    Args:
        fahrenheit_temp: Temperature in Fahrenheit
        
    Returns:
        Temperature in Celsius
        
    Raises:
        TypeError: If input is not a number
    """
    if not isinstance(fahrenheit_temp, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    return (float(fahrenheit_temp) - 32) * 5/9


def kelvin_to_fahrenheit(kelvin_temp: Union[int, float, Decimal]) -> float:
    """
    Convert temperature from Kelvin to Fahrenheit.
    
    Args:
        kelvin_temp: Temperature in Kelvin
        
    Returns:
        Temperature in Fahrenheit
        
    Raises:
        ValueError: If temperature is below absolute zero
        TypeError: If input is not a number
    """
    if not isinstance(kelvin_temp, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    if kelvin_temp < 0:
        raise ValueError("Temperature cannot be below absolute zero")
    
    celsius_temp = kelvin_to_celsius(kelvin_temp)
    return celsius_to_fahrenheit(celsius_temp)


def fahrenheit_to_kelvin(fahrenheit_temp: Union[int, float, Decimal]) -> float:
    """
    Convert temperature from Fahrenheit to Kelvin.
    
    Args:
        fahrenheit_temp: Temperature in Fahrenheit
        
    Returns:
        Temperature in Kelvin
        
    Raises:
        TypeError: If input is not a number
    """
    if not isinstance(fahrenheit_temp, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    celsius_temp = fahrenheit_to_celsius(fahrenheit_temp)
    return celsius_to_kelvin(celsius_temp)


def convert_temperature(temperature: Union[int, float, Decimal], 
                       from_unit: str, 
                       to_unit: str) -> float:
    """
    Universal temperature converter supporting multiple units.
    
    Args:
        temperature: Temperature value to convert
        from_unit: Source unit ('celsius', 'fahrenheit', 'kelvin')
        to_unit: Target unit ('celsius', 'fahrenheit', 'kelvin')
        
    Returns:
        Converted temperature value
        
    Raises:
        ValueError: If units are invalid or conversion is impossible
        TypeError: If temperature is not a number
    """
    if not isinstance(temperature, (int, float, Decimal)):
        raise TypeError("Temperature must be a number")
    
    # Normalize unit names
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()
    
    valid_units = {'celsius', 'fahrenheit', 'kelvin'}
    if from_unit not in valid_units:
        raise ValueError(f"Invalid source unit: {from_unit}")
    if to_unit not in valid_units:
        raise ValueError(f"Invalid target unit: {to_unit}")
    
    # Direct conversion if same units
    if from_unit == to_unit:
        return float(temperature)
    
    # Conversion mapping
    conversions = {
        ('celsius', 'kelvin'): celsius_to_kelvin,
        ('celsius', 'fahrenheit'): celsius_to_fahrenheit,
        ('kelvin', 'celsius'): kelvin_to_celsius,
        ('kelvin', 'fahrenheit'): kelvin_to_fahrenheit,
        ('fahrenheit', 'celsius'): fahrenheit_to_celsius,
        ('fahrenheit', 'kelvin'): fahrenheit_to_kelvin,
    }
    
    conversion_func = conversions.get((from_unit, to_unit))
    if conversion_func:
        return conversion_func(temperature)
    else:
        raise ValueError(f"Conversion from {from_unit} to {to_unit} not supported")


def format_temperature(temperature: Union[int, float], 
                      unit: str = 'celsius', 
                      decimal_places: int = 1) -> str:
    """
    Format temperature with appropriate unit symbol.
    
    Args:
        temperature: Temperature value
        unit: Temperature unit ('celsius', 'fahrenheit', 'kelvin')
        decimal_places: Number of decimal places to display
        
    Returns:
        Formatted temperature string with unit symbol
        
    Raises:
        ValueError: If unit is invalid
    """
    unit = unit.lower().strip()
    
    unit_symbols = {
        'celsius': '°C',
        'fahrenheit': '°F', 
        'kelvin': 'K'
    }
    
    if unit not in unit_symbols:
        raise ValueError(f"Invalid unit: {unit}")
    
    rounded_temp = round(float(temperature), decimal_places)
    symbol = unit_symbols[unit]
    
    return f"{rounded_temp}{symbol}"


def convert_weather_data(weather_data: Dict[str, Any], 
                        target_unit: str = 'celsius',
                        source_unit: str = 'celsius') -> Dict[str, Any]:
    """
    Convert temperature values in weather data dict to target unit.
    
    Args:
        weather_data: Weather data dictionary containing temperature values
        target_unit: Target temperature unit
        source_unit: Source temperature unit of the input data
        
    Returns:
        Weather data with converted temperature values
        
    Raises:
        ValueError: If target unit is invalid
    """
    if not isinstance(weather_data, dict):
        raise TypeError("Weather data must be a dictionary")
    
    target_unit = target_unit.lower().strip()
    source_unit = source_unit.lower().strip()
    
    if target_unit not in {'celsius', 'fahrenheit', 'kelvin'}:
        raise ValueError(f"Invalid target unit: {target_unit}")
    if source_unit not in {'celsius', 'fahrenheit', 'kelvin'}:
        raise ValueError(f"Invalid source unit: {source_unit}")
    
    # Copy the original data to avoid mutation
    converted_data = weather_data.copy()
    
    # Temperature fields that might need conversion
    temp_fields = ['temperature', 'temp', 'feels_like', 'temp_min', 'temp_max']
    
    for field in temp_fields:
        if field in converted_data:
            try:
                source_temp = float(converted_data[field])
                converted_temp = convert_temperature(source_temp, source_unit, target_unit)
                converted_data[field] = round(converted_temp, 1)
            except (ValueError, TypeError):
                # Skip conversion if temperature is invalid
                continue
    
    # Add unit information to data
    converted_data['temperature_unit'] = target_unit
    
    return converted_data