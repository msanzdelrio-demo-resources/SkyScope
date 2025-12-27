#!/usr/bin/env python
"""
Quick test runner for Fahrenheit temperature support tests.

This script provides convenient commands to run the comprehensive
test suite created for Fahrenheit temperature display feature.
"""

import subprocess
import sys


def run_command(cmd, description):
    """Run a command and report results."""
    print(f"\n{'='*70}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*70)
    
    result = subprocess.run(cmd)
    return result.returncode


def main():
    """Run test suite commands."""
    
    commands = {
        '1': {
            'description': 'Run ALL tests (complete suite)',
            'cmd': [sys.executable, '-m', 'pytest', 'tests/', '-v', '--tb=short']
        },
        '2': {
            'description': 'Run only Fahrenheit unit validation tests',
            'cmd': [sys.executable, '-m', 'pytest', 
                   'tests/unit/test_fahrenheit_unit_validation.py', '-v']
        },
        '3': {
            'description': 'Run temperature conversion tests (including Fahrenheit)',
            'cmd': [sys.executable, '-m', 'pytest', 
                   'tests/unit/test_temperature_conversion.py', '-v']
        },
        '4': {
            'description': 'Run temperature display formatting tests',
            'cmd': [sys.executable, '-m', 'pytest', 
                   'tests/unit/test_temperature_display_formatting.py', '-v']
        },
        '5': {
            'description': 'Run Fahrenheit UI functional tests',
            'cmd': [sys.executable, '-m', 'pytest', 
                   'tests/functional/test_temperature_ui.py::TestFahrenheitUIIntegration', '-v']
        },
        '6': {
            'description': 'Run Fahrenheit API integration tests',
            'cmd': [sys.executable, '-m', 'pytest', 
                   'tests/integration/test_temperature_api.py::TestFahrenheitAPIIntegration', '-v']
        },
        '7': {
            'description': 'Run all tests with coverage report',
            'cmd': [sys.executable, '-m', 'pytest', 'tests/', 
                   '--cov=app', '--cov-report=html', '-v']
        },
        '8': {
            'description': 'Run quick sanity check (subset of critical tests)',
            'cmd': [sys.executable, '-m', 'pytest', 
                   'tests/unit/test_temperature_conversion.py::TestTemperatureConversion::test_fahrenheit_conversion_complete_coverage',
                   'tests/unit/test_fahrenheit_unit_validation.py::TestFahrenheitUnitValidation::test_fahrenheit_api_parameter_mapping',
                   'tests/integration/test_temperature_api.py::TestFahrenheitAPIIntegration::test_fahrenheit_api_units_parameter_imperial',
                   '-v']
        },
    }
    
    print("\n" + "="*70)
    print("Fahrenheit Temperature Support - Test Runner")
    print("="*70)
    print("\nSelect a test suite to run:\n")
    
    for key, value in commands.items():
        print(f"  {key}. {value['description']}")
    
    print("\n  q. Quit")
    print("\n" + "-"*70)
    
    choice = input("\nEnter your choice (1-8 or q): ").strip().lower()
    
    if choice == 'q' or choice == 'quit':
        print("Exiting.")
        return 0
    
    if choice not in commands:
        print(f"Invalid choice: {choice}")
        return 1
    
    cmd = commands[choice]
    return run_command(cmd['cmd'], cmd['description'])


if __name__ == '__main__':
    sys.exit(main())
