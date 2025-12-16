# SkyScope Temperature Unit Toggle - Test Suite

This directory contains comprehensive test suites for the temperature unit toggle feature implementation in SkyScope.

## 📁 Test Structure

```
tests/
├── __init__.py                    # Test package initialization
├── conftest.py                    # Common test configuration and base classes
├── run_tests.py                   # Test runner and coverage utilities
├── unit/                          # Unit tests (isolated component testing)
│   ├── __init__.py
│   ├── test_temperature_conversion.py    # Temperature conversion utilities
│   └── test_session_management.py        # Session management functionality
├── integration/                   # Integration tests (component interaction)
│   ├── __init__.py
│   └── test_temperature_api.py           # API integration and workflows
├── functional/                    # Functional tests (user-facing features)
│   ├── __init__.py
│   └── test_temperature_ui.py            # UI components and accessibility
└── fixtures/                      # Test data and fixtures
    ├── __init__.py
    └── sample_data.py                     # Comprehensive test data
```

## 🎯 Test Coverage Goals

- **>95% Code Coverage** for temperature-related features
- **Temperature Conversion Accuracy** within ±0.1°
- **Performance Requirements** - conversions <10ms
- **Cross-browser Compatibility** - Chrome, Firefox, Safari, Edge
- **Accessibility Compliance** - WCAG 2.1 AA standards

## 🧪 Test Categories

### Unit Tests (`tests/unit/`)

**Temperature Conversion (`test_temperature_conversion.py`)**
- Kelvin ↔ Celsius conversion accuracy
- Celsius ↔ Fahrenheit conversion accuracy
- Universal temperature converter
- Edge cases and extreme temperatures
- Performance benchmarks
- Input validation and error handling

**Session Management (`test_session_management.py`)**
- Temperature unit preference storage
- Session persistence across requests
- Default temperature unit behavior (Celsius)
- Session security and sanitization
- `/set-temperature-unit` endpoint functionality

### Integration Tests (`tests/integration/`)

**API Integration (`test_temperature_api.py`)**
- OpenWeatherMap API calls with unit parameters
- Temperature data processing and formatting
- API error handling and resilience
- End-to-end workflow testing
- Mock API response handling

### Functional Tests (`tests/functional/`)

**UI Components (`test_temperature_ui.py`)**
- Temperature toggle switch rendering
- Unit change interactions
- State synchronization with backend
- Accessibility testing (ARIA, keyboard navigation)
- Performance testing (response times)
- Cross-browser compatibility
- Error handling and user feedback

## 🏃‍♂️ Running Tests

### All Tests
```bash
python tests/run_tests.py
```

### By Category
```bash
python tests/run_tests.py unit         # Unit tests only
python tests/run_tests.py integration  # Integration tests only
python tests/run_tests.py functional   # Functional tests only
```

### With Coverage Report
```bash
python tests/run_tests.py coverage
```

### Using pytest (recommended)
```bash
# Install pytest and coverage
pip install pytest pytest-cov

# Run all tests with coverage
pytest tests/ -v --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit/ -v
pytest tests/integration/ -v
pytest tests/functional/ -v
```

## 📊 Coverage Reporting

Coverage reports are generated in multiple formats:
- **Terminal output** - Summary statistics
- **HTML report** - Detailed line-by-line coverage in `htmlcov/`
- **Coverage data** - Raw coverage data in `.coverage`

## 🔧 Test Configuration

### Base Test Case (`conftest.py`)
- Common Flask test client setup
- Test database configuration
- Session handling utilities
- Mock API response classes

### Mock Data (`fixtures/sample_data.py`)
- Weather data for major cities
- Extreme temperature scenarios
- API error responses
- Session test data
- UI test fixtures

## 🌡️ Temperature Test Data

### Real-world Cities
- London (15°C), New York (25°C), Tokyo (28°C)
- Sydney (20°C), Mumbai (35°C), Moscow (-5°C)
- Reykjavik (2°C), Dubai (40°C)

### Extreme Scenarios
- Death Valley (55°C/131°F)
- Antarctica (-50°C/-58°F)
- Sahara Desert (50°C/122°F)
- Siberian Winter (-40°C/-40°F)

### Conversion Test Points
- Absolute zero (0K/-273.15°C/-459.67°F)
- Water freezing (273.15K/0°C/32°F)
- Water boiling (373.15K/100°C/212°F)
- Room temperature (288.15K/15°C/59°F)
- Human body (310.15K/37°C/98.6°F)

## 🔐 Security Testing

### Input Validation
- Temperature unit parameter validation
- Session data sanitization
- XSS prevention testing
- SQL injection prevention

### Session Security
- Session data encryption
- CSRF protection validation
- Session timeout handling
- Concurrent session management

## ♿ Accessibility Testing

### WCAG 2.1 AA Compliance
- Keyboard navigation support
- Screen reader compatibility
- Color contrast validation
- ARIA label verification
- Semantic HTML structure

### Testing Tools
- Automated accessibility scanning
- Keyboard navigation testing
- Screen reader simulation
- Color contrast analysis

## 🚀 Performance Testing

### Benchmarks
- Temperature conversion: <10ms
- Page load time: <1 second
- AJAX responses: <500ms
- API responses: <3 seconds

### Load Testing
- Concurrent user simulation
- Rate limiting validation
- Memory usage monitoring
- Response time analysis

## 🌍 Cross-browser Testing

### Supported Browsers
- **Chrome** - Latest 2 versions
- **Firefox** - Latest 2 versions  
- **Safari** - Latest 2 versions
- **Edge** - Latest 2 versions

### Mobile Support
- Mobile Chrome (Android)
- Mobile Safari (iOS)
- Responsive design validation

## 🚨 Error Handling Tests

### API Errors
- Network connectivity issues
- Invalid API responses
- Rate limiting scenarios
- Service unavailability

### UI Error States
- JavaScript failure graceful degradation
- Form validation feedback
- Network error user messaging
- Session expiration handling

## 📈 Continuous Integration

### GitHub Actions Integration
```yaml
# .github/workflows/test.yml
- name: Run Temperature Tests
  run: |
    pip install -r requirements.txt
    python tests/run_tests.py coverage
    
- name: Upload Coverage
  uses: codecov/codecov-action@v1
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Run tests before commits
pre-commit install
```

## 🔍 Test Debugging

### Verbose Output
```bash
pytest tests/ -v -s  # Show print statements
```

### Debug Specific Tests
```bash
pytest tests/unit/test_temperature_conversion.py::TestTemperatureConversion::test_kelvin_to_celsius_accuracy -v
```

### Coverage Analysis
```bash
coverage report --show-missing  # Show uncovered lines
coverage html                   # Generate detailed HTML report
```

## 📝 Test Documentation

Each test file includes:
- **Purpose** - What functionality is being tested
- **Coverage** - What scenarios are covered
- **Dependencies** - External services or mocks required
- **Setup** - Special configuration needed

### Example Test Documentation
```python
"""
Unit tests for temperature conversion utilities.

Test Coverage:
- kelvin_to_celsius() accuracy (±0.1°)
- celsius_to_kelvin() accuracy
- convert_temperature() universal converter
- Edge cases (extreme temperatures, invalid inputs)
- Performance testing (<10ms conversion time)
"""
```

## 🎯 Quality Assurance Checklist

### Test Completeness
- [ ] All acceptance criteria have corresponding tests
- [ ] All edge cases are covered
- [ ] Both success and failure paths are tested
- [ ] All new code has test coverage

### Test Quality
- [ ] Tests are independent and isolated
- [ ] Test names clearly describe what is being tested
- [ ] Tests follow consistent patterns and conventions
- [ ] Appropriate assertions are used
- [ ] Test data is realistic and comprehensive

### Performance and Reliability
- [ ] Tests run efficiently and complete within reasonable time
- [ ] Tests are reliable and don't produce false positives
- [ ] Resource cleanup is properly handled
- [ ] Tests can run in any order

## 🔗 Integration with Development Plan

These tests align with the 5 GitHub issues for temperature unit toggle:

1. **Issue #58** - Backend Temperature Unit Management System
   - `test_session_management.py` - Session handling
   - `test_temperature_conversion.py` - Conversion utilities

2. **Issue #59** - Frontend Temperature Unit Toggle Interface  
   - `test_temperature_ui.py` - UI components and interactions

3. **Issue #60** - Enhanced Weather Data Display with Unit Awareness
   - `test_temperature_api.py` - API integration and display

4. **Issue #61** - Comprehensive Testing Suite for Temperature Features
   - **This entire test suite** validates the implementation

5. **Issue #62** - Documentation and Deployment Preparation
   - Test documentation and CI/CD integration

## 📞 Support

For questions about the test suite:
- Review test documentation in each file
- Check `conftest.py` for common utilities
- Examine `fixtures/sample_data.py` for test data
- Run tests with `-v` flag for detailed output

---

**Ready for Implementation**: These tests provide comprehensive validation for the temperature unit toggle feature as development progresses through the 5 GitHub issues.