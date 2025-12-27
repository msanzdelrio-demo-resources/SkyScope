# SkyScope

This is a simple weather application built with Flask. It allows users to enter a city name and get the current weather information for that city, with support for both Celsius and Kelvin temperature displays.

## 🌡️ Temperature Unit Toggle Feature

### Overview
SkyScope now supports switching between Celsius (°C) and Kelvin (K) temperature displays with a convenient toggle switch. Users can seamlessly switch between temperature units and their preference is saved for the session.

### Usage
1. Enter a city name and get weather information
2. Use the temperature unit toggle switch located near the temperature display
3. Choose between °C (Celsius) and K (Kelvin) units
4. Your preference is automatically saved for the session
5. All temperature values (current, feels-like, etc.) update instantly

### Features
- **Interactive Toggle**: Modern slider switch with smooth animations
- **Session Persistence**: Your temperature unit preference is remembered during your session
- **Instant Updates**: All temperature values convert immediately when switching units
- **Consistent Display**: All temperature-related metrics use the same unit
- **Accessibility**: Full keyboard navigation and screen reader support

# Installation

1. Clone the repository:
```sh
git clone https://github.com/msanzdelrio-demo-resources/SkyScope.git
```
2. Navigate to the project directory:
```sh
cd SkyScope
```
3. Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
4. Install the required Python packages:
```sh
pip install -r requirements.txt
```
5. Set up your OpenWeatherMap API key:
   - Create a `.env` file in the project root (copy from `.env.example`)
   - Add your API key: `OPENWEATHER_APPID=your_api_key_here`
   - Add a strong secret key: `SECRET_KEY=your_secret_key_here`
   - **⚠️ CRITICAL SECURITY:** Never commit your `.env` file or hardcode API keys in code!

## API Documentation

### Weather Endpoints
- **GET/POST** `/` - Main weather display page
  - **POST Body**: `{"city": "London"}`
  - **Response**: HTML page with weather data

### Temperature Unit Management
- **POST** `/set-temperature-unit` - Update temperature unit preference
  - **Content-Type**: `application/json`
  - **Request Body**: 
    ```json
    {"unit": "celsius" | "kelvin"}
    ```
  - **Response**: 
    ```json
    {"success": true, "unit": "celsius"}
    ```
  - **Error Response**: 
    ```json
    {"success": false, "error": "Invalid unit"}
    ```

# Usage

To run the application, execute the following command in the project directory:
```sh
source venv/bin/activate  # Activate virtual environment
python run.py
```
Then, open your web browser and navigate to http://localhost:5001.

### Using the Temperature Toggle
1. **Get Weather Data**: Enter a city name and click "Get Weather"
2. **Switch Units**: Use the toggle switch near the temperature display
   - **Left position (°C)**: Shows temperatures in Celsius
   - **Right position (K)**: Shows temperatures in Kelvin
3. **Automatic Updates**: All temperature values update instantly
4. **Session Memory**: Your preference is saved until you close the browser

# Files

- **app/views.py**: Contains the Flask routes and the main logic of the application
- **app/utils.py**: Temperature conversion utilities and weather data processing
- **app/templates/index.html**: The HTML template for the main page with temperature toggle
- **app/static/css/style.css**: The CSS styles including toggle switch styling
- **app/static/js/main.js**: JavaScript for form submission and temperature unit toggle
- **tests/unit/test_temperature_conversion.py**: Comprehensive unit tests for temperature features
- **tests/test_views.py**: Integration tests for the application routes

## 🔒 Security

### API Key Security
**CRITICAL:** API keys must NEVER be committed to version control or hardcoded in code.

✅ **DO:**
- Store API keys in `.env` file (already in `.gitignore`)
- Use environment variables for all secrets
- Generate strong secret keys for production
- Keep `.env.example` updated (without actual values)

❌ **DON'T:**
- Hardcode API keys in JavaScript, HTML, or Python files
- Commit `.env` file to Git
- Share API keys in pull requests or issues
- Use weak or default secret keys in production

### Environment Configuration

**Development Mode (default):**
```bash
export FLASK_ENV=development
python run.py
```

**Production Mode:**
```bash
export FLASK_ENV=production
export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
export OPENWEATHER_APPID=your_actual_api_key
python run.py
```

### Production Security Checklist
- [ ] Set `FLASK_ENV=production`
- [ ] Set strong `SECRET_KEY` (64 characters minimum)
- [ ] Configure HTTPS/SSL certificate
- [ ] Enable rate limiting
- [ ] Set up monitoring and logging
- [ ] Review security headers
- [ ] Run security scan: `python security_check.py`
- [ ] Update all dependencies
- [ ] Configure firewall rules

### Security Scanning

Run security checks before deployment:
```bash
# Install security tools
pip install safety bandit

# Check for vulnerable dependencies
safety check

# Scan code for security issues
bandit -r app/

# Or run comprehensive check
python security_check.py
```

## Testing

To run the tests, execute the following command in the project directory:
```sh
source venv/bin/activate
python -m pytest tests/ -v
```

### Test Coverage
- **Temperature Conversion**: 15 comprehensive unit tests with >95% coverage
- **API Endpoints**: Integration tests for weather and temperature unit routes  
- **Frontend Functionality**: Manual testing for toggle interactions
- **Security**: CSRF protection and input validation testing

### Running Specific Tests
```sh
# Temperature conversion tests only
python -m pytest tests/unit/test_temperature_conversion.py -v

# All unit tests
python -m unittest discover tests
```

Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

License

MIT (https://choosealicense.com/licenses/mit/)


## How to test it locally

1. Clone the repository:
```sh
git clone https://github.com/msanzdelrio-demo-resources/SkyScope.git
```
2. Navigate to the project directory:
```sh
cd SkyScope
```
3. Create and activate virtual environment:
```sh
python -m venv venv
source venv/bin/activate
```
4. Install the required Python packages:
```sh
pip install -r requirements.txt
```
5. Set up environment variables:
```sh
# Create .env file with your OpenWeatherMap API key
echo "OPENWEATHERMAP_API_KEY=your_api_key_here" > .env
```
6. Run the application:
```sh
python run.py
```
7. Open your web browser and navigate to http://localhost:5001
8. **Test Weather Functionality**:
   - Enter a city name in the input field and click "Get Weather"
   - Verify that weather information displays correctly
9. **Test Temperature Toggle**:
   - Use the toggle switch to switch between °C and K
   - Verify all temperature values update immediately
   - Refresh the page and confirm your unit preference is maintained

### Environment Variables
Create a `.env` file in the project root with:
```env
OPENWEATHERMAP_API_KEY=your_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_for_sessions
```


## Features

- **Real-time Weather Data**: Current weather conditions from OpenWeatherMap API
- **Temperature Unit Toggle**: Switch between Celsius (°C) and Kelvin (K) instantly
- **Session Persistence**: Temperature unit preference saved during browser session
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Security Features**: CSRF protection, input validation, and secure session management
- **Comprehensive Testing**: >95% test coverage with unit and integration tests
- **Accessibility**: Screen reader support and keyboard navigation

## Security

SkyScope includes enterprise-grade security features:
- **CSRF Protection**: Prevents cross-site request forgery attacks
- **Input Validation**: Comprehensive sanitization of user inputs
- **Secure Sessions**: Encrypted session management for user preferences
- **Security Headers**: X-Frame-Options, X-Content-Type-Options, and more
- **Environment Variables**: Secure API key and configuration management

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/temperature-enhancement`)
3. Make your changes and add tests
4. Ensure all tests pass (`python -m pytest tests/ -v`)
5. Commit your changes (`git commit -am 'Add temperature enhancement'`)
6. Push to the branch (`git push origin feature/temperature-enhancement`)
7. Create a Pull Request

## License

[MIT](https://choosealicense.com/licenses/mit/)
