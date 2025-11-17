// Temperature Unit Toggle Functionality
(function() {
    'use strict';

    // Temperature conversion functions
    function celsiusToFahrenheit(celsius) {
        return Math.round((celsius * 9/5 + 32) * 10) / 10;
    }

    function fahrenheitToCelsius(fahrenheit) {
        return Math.round(((fahrenheit - 32) * 5/9) * 10) / 10;
    }

    // Initialize temperature unit preference
    function initTemperatureUnit() {
        const toggleButton = document.getElementById('unit-toggle');
        const temperatureValue = document.getElementById('temperature-value');
        const temperatureUnit = document.getElementById('temperature-unit');
        
        // Check if elements exist (only on weather results page)
        if (!toggleButton || !temperatureValue || !temperatureUnit) {
            return;
        }

        // Get stored preference or default to Celsius
        const savedUnit = localStorage.getItem('temperatureUnit') || 'celsius';
        const celsiusTemp = parseFloat(temperatureValue.dataset.celsius);

        // Apply saved preference
        if (savedUnit === 'fahrenheit') {
            const fahrenheitTemp = celsiusToFahrenheit(celsiusTemp);
            temperatureValue.textContent = fahrenheitTemp;
            temperatureUnit.textContent = '°F';
            toggleButton.classList.add('fahrenheit');
            toggleButton.setAttribute('aria-checked', 'true');
        } else {
            temperatureValue.textContent = celsiusTemp;
            temperatureUnit.textContent = '°C';
            toggleButton.classList.remove('fahrenheit');
            toggleButton.setAttribute('aria-checked', 'false');
        }

        // Add click event listener
        toggleButton.addEventListener('click', function() {
            const isFahrenheit = toggleButton.classList.contains('fahrenheit');
            
            if (isFahrenheit) {
                // Switch to Celsius
                temperatureValue.textContent = celsiusTemp;
                temperatureUnit.textContent = '°C';
                toggleButton.classList.remove('fahrenheit');
                toggleButton.setAttribute('aria-checked', 'false');
                localStorage.setItem('temperatureUnit', 'celsius');
            } else {
                // Switch to Fahrenheit
                const fahrenheitTemp = celsiusToFahrenheit(celsiusTemp);
                temperatureValue.textContent = fahrenheitTemp;
                temperatureUnit.textContent = '°F';
                toggleButton.classList.add('fahrenheit');
                toggleButton.setAttribute('aria-checked', 'true');
                localStorage.setItem('temperatureUnit', 'fahrenheit');
            }
        });

        // Add keyboard support for accessibility
        toggleButton.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                toggleButton.click();
            }
        });
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initTemperatureUnit);
    } else {
        initTemperatureUnit();
    }
})();

document.getElementById('weatherForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var city = document.getElementById('city').value;
    fetch('/weather?city=' + city)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            document.getElementById('weatherInfo').textContent = 'Weather in ' + city + ': ' + data.weather;
            document.getElementById('windSpeed').textContent = 'Wind Speed: ' + data.wind_speed + ' m/s';
            document.getElementById('rain').textContent = 'Rain: ' + data.rain + ' %';
            document.getElementById('pressure').textContent = 'Pressure: ' + data.pressure + ' hPa';
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
});