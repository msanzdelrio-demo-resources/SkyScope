"""
Test runner for SkyScope temperature unit toggle test suite.

This module provides utilities to run all temperature-related tests
and generate coverage reports.

Usage:
    python -m pytest tests/ -v --cov=app --cov-report=html
    python tests/run_tests.py
"""

import unittest
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tests.unit.test_temperature_conversion import TestTemperatureConversion, TestThreeWayConversionScenarios
from tests.unit.test_session_management import TestSessionManagement, TestSetTemperatureUnitEndpoint
from tests.integration.test_temperature_api import (
    TestTemperatureAwareAPI, 
    TestEndToEndTemperatureWorkflow,
    TestTemperatureUnitSessionPersistence,
    TestFahrenheitEdgeCases
)
from tests.functional.test_temperature_ui import (
    TestTemperatureUIComponents, 
    TestTemperatureUIAccessibility,
    TestTemperatureUIPerformance,
    TestCrossBrowserCompatibility,
    TestTemperatureUIErrorHandling
)


def create_test_suite():
    """Create comprehensive test suite for temperature functionality."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Unit Tests
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestThreeWayConversionScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestSetTemperatureUnitEndpoint))
    
    # Integration Tests
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureAwareAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndTemperatureWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUnitSessionPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestFahrenheitEdgeCases))
    
    # Functional Tests
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIComponents))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIAccessibility))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossBrowserCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIErrorHandling))
    
    return suite


def run_unit_tests():
    """Run only unit tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureConversion))
    suite.addTests(loader.loadTestsFromTestCase(TestThreeWayConversionScenarios))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionManagement))
    suite.addTests(loader.loadTestsFromTestCase(TestSetTemperatureUnitEndpoint))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_integration_tests():
    """Run only integration tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureAwareAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndTemperatureWorkflow))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUnitSessionPersistence))
    suite.addTests(loader.loadTestsFromTestCase(TestFahrenheitEdgeCases))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_functional_tests():
    """Run only functional tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIComponents))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIAccessibility))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIPerformance))
    suite.addTests(loader.loadTestsFromTestCase(TestCrossBrowserCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestTemperatureUIErrorHandling))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def run_all_tests():
    """Run complete test suite."""
    suite = create_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


def generate_coverage_report():
    """Generate code coverage report."""
    try:
        import coverage
        
        # Initialize coverage
        cov = coverage.Coverage()
        cov.start()
        
        # Run tests
        success = run_all_tests()
        
        # Stop coverage and generate report
        cov.stop()
        cov.save()
        
        print("\n" + "="*50)
        print("COVERAGE REPORT")
        print("="*50)
        cov.report()
        
        # Generate HTML report
        cov.html_report(directory='htmlcov')
        print(f"\nHTML coverage report generated in: {project_root}/htmlcov/")
        
        return success
        
    except ImportError:
        print("Coverage.py not installed. Install with: pip install coverage")
        return run_all_tests()


def main():
    """Main test runner."""
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
        
        if test_type == 'unit':
            success = run_unit_tests()
        elif test_type == 'integration':
            success = run_integration_tests()
        elif test_type == 'functional':
            success = run_functional_tests()
        elif test_type == 'coverage':
            success = generate_coverage_report()
        else:
            print("Usage: python run_tests.py [unit|integration|functional|coverage]")
            sys.exit(1)
    else:
        success = run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()