/**
 * SkyScope Temperature Toggle and Weather Display
 * Handles temperature unit conversion and UI interactions
 */

class TemperatureConverter {
    constructor() {
        this.conversions = {
            celsius: {
                fahrenheit: (c) => (c * 9/5) + 32,
                kelvin: (c) => c + 273.15,
                celsius: (c) => c
            },
            fahrenheit: {
                celsius: (f) => (f - 32) * 5/9,
                kelvin: (f) => ((f - 32) * 5/9) + 273.15,
                fahrenheit: (f) => f
            },
            kelvin: {
                celsius: (k) => k - 273.15,
                fahrenheit: (k) => ((k - 273.15) * 9/5) + 32,
                kelvin: (k) => k
            }
        };
        
        this.symbols = {
            celsius: '°C',
            fahrenheit: '°F',
            kelvin: 'K'
        };
    }
    
    convert(temperature, fromUnit, toUnit) {
        if (!this.conversions[fromUnit] || !this.conversions[fromUnit][toUnit]) {
            throw new Error(`Conversion from ${fromUnit} to ${toUnit} not supported`);
        }
        
        return this.conversions[fromUnit][toUnit](temperature);
    }
    
    format(temperature, unit, decimalPlaces = 1) {
        const rounded = Math.round(temperature * Math.pow(10, decimalPlaces)) / Math.pow(10, decimalPlaces);
        return `${rounded}${this.symbols[unit]}`;
    }
}

class SkyScope {
    constructor() {
        this.converter = new TemperatureConverter();
        this.currentUnit = this.getCurrentUnit();
        this.weatherData = window.weatherData || null;
        
        this.initializeToggle();
        this.initializeForm();
        this.syncToggleWithServer();
    }
    
    getCurrentUnit() {
        // Get from checkbox toggle or default to celsius
        const toggle = document.getElementById('temp-unit-toggle');
        return toggle && toggle.checked ? 'kelvin' : 'celsius';
    }
    
    syncToggleWithServer() {
        // Set the toggle state based on the temperature unit from the server
        const toggle = document.getElementById('temp-unit-toggle');
        const serverUnit = document.body.getAttribute('data-temperature-unit') || 'celsius';
        if (toggle) {
            toggle.checked = serverUnit === 'kelvin';
            this.currentUnit = serverUnit;
        }
    }
    
    initializeToggle() {
        const toggle = document.getElementById('temp-unit-toggle');
        
        if (toggle) {
            toggle.addEventListener('change', (e) => {
                const newUnit = e.target.checked ? 'kelvin' : 'celsius';
                this.handleUnitChange(newUnit);
            });
            
            // Add keyboard navigation support
            toggle.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    e.target.checked = !e.target.checked;
                    const newUnit = e.target.checked ? 'kelvin' : 'celsius';
                    this.handleUnitChange(newUnit);
                }
            });
        }
    }
    
    initializeForm() {
        const form = document.getElementById('weatherForm');
        if (form) {
            form.addEventListener('submit', (e) => {
                this.handleFormSubmit(e);
            });
        }
    }
    
    async handleUnitChange(newUnit) {
        const previousUnit = this.currentUnit;
        this.currentUnit = newUnit;
        
        try {
            console.log(`Temperature unit changing from ${previousUnit} to ${newUnit}`);
            
            // Update session with new temperature unit
            await this.updateTemperatureUnit(newUnit);
            console.log('Temperature unit session updated successfully');
            
            // If weather data exists, resubmit the form to get updated temperatures
            const currentCity = document.getElementById('city')?.value;
            if (currentCity && currentCity.trim()) {
                console.log('Resubmitting form for city:', currentCity);
                // Trigger form submission to reload weather with new units
                const form = document.getElementById('weatherForm');
                if (form) {
                    form.requestSubmit();
                }
            } else {
                console.log('No city data, just showing success message');
            }
            
            // Show feedback
            this.showToast(`Temperature unit changed to ${newUnit.charAt(0).toUpperCase() + newUnit.slice(1)}`);
            
        } catch (error) {
            console.error('Error changing temperature unit:', error);
            this.showToast('Error changing temperature unit', 'error');
            
            // Revert toggle state on error
            const toggle = document.getElementById('temp-unit-toggle');
            if (toggle) {
                toggle.checked = previousUnit === 'kelvin';
            }
            this.currentUnit = previousUnit;
        }
    }
    
    async updateTemperatureUnit(unit) {
        console.log('Sending temperature unit update request:', unit);
        
        // Get CSRF token from form
        const csrfToken = document.querySelector('input[name=csrf_token]')?.value;
        
        if (!csrfToken) {
            console.error('CSRF token not found');
            throw new Error('CSRF token not found');
        }
        
        const headers = {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken
        };
        
        const response = await fetch('/set-temperature-unit', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({ unit: unit })
        });
        
        console.log('Temperature unit update response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        console.log('Temperature unit update result:', result);
        
        if (!result.success) {
            throw new Error(result.error || 'Failed to update temperature unit');
        }
        
        return result;
    }
    
    updateTemperatureDisplay(fromUnit, toUnit) {
        if (!this.weatherData || fromUnit === toUnit) return;
        
        try {
            // Update main temperature
            const mainTempElement = document.getElementById('main-temp');
            if (mainTempElement && this.weatherData.temperature !== undefined) {
                const convertedTemp = this.converter.convert(this.weatherData.temperature, fromUnit, toUnit);
                mainTempElement.textContent = this.converter.format(convertedTemp, toUnit);
                this.weatherData.temperature = convertedTemp;
            }
            
            // Update feels like temperature
            const feelsLikeTempElement = document.getElementById('feels-like-temp');
            if (feelsLikeTempElement && this.weatherData.feels_like !== undefined) {
                const convertedFeelsLike = this.converter.convert(this.weatherData.feels_like, fromUnit, toUnit);
                feelsLikeTempElement.textContent = this.converter.format(convertedFeelsLike, toUnit);
                this.weatherData.feels_like = convertedFeelsLike;
            }
            
            // Update min temperature
            const minTempElement = document.getElementById('min-temp');
            if (minTempElement && this.weatherData.temp_min !== undefined) {
                const convertedMin = this.converter.convert(this.weatherData.temp_min, fromUnit, toUnit);
                minTempElement.textContent = this.converter.format(convertedMin, toUnit);
                this.weatherData.temp_min = convertedMin;
            }
            
            // Update max temperature
            const maxTempElement = document.getElementById('max-temp');
            if (maxTempElement && this.weatherData.temp_max !== undefined) {
                const convertedMax = this.converter.convert(this.weatherData.temp_max, fromUnit, toUnit);
                maxTempElement.textContent = this.converter.format(convertedMax, toUnit);
                this.weatherData.temp_max = convertedMax;
            }
            
            // Update the current unit in weather data
            this.weatherData.current_unit = toUnit;
            
        } catch (error) {
            console.error('Error updating temperature display:', error);
            throw error;
        }
    }
    
    handleFormSubmit(e) {
        const submitButton = e.target.querySelector('input[type="submit"]');
        const cityInput = e.target.querySelector('#city');
        
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.value = 'Loading...';
        }
        
        // Validate city input - updated pattern to match backend validation
        if (cityInput) {
            const city = cityInput.value.trim();
            // Use backend-provided city pattern if available, else fallback to default
            const cityPattern = window.CITY_PATTERN
                ? new RegExp(window.CITY_PATTERN)
                : /^[a-zA-Z\s\-',.0-9]{1,64}$/;
            
            if (!city || !cityPattern.test(city)) {
                e.preventDefault();
                this.showToast('Please enter a valid city name (letters, numbers, spaces, and basic punctuation only)', 'error');
                
                if (submitButton) {
                    submitButton.disabled = false;
                    submitButton.value = 'Get Weather';
                }
                return false;
            }
        }
        
        // Form will submit normally, let the backend handle the response
        // Re-enable button after a delay in case of client-side issues
        setTimeout(() => {
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.value = 'Get Weather';
            }
        }, 3000);
    }
    
    showToast(message, type = 'info') {
        // Sanitize message to prevent XSS
        const sanitizedMessage = message.replace(/[<>"'&]/g, function(char) {
            const entities = {
                '<': '&lt;',
                '>': '&gt;',
                '"': '&quot;',
                "'": '&#x27;',
                '&': '&amp;'
            };
            return entities[char] || char;
        });
        
        // Remove existing toasts
        const existingToasts = document.querySelectorAll('.toast');
        existingToasts.forEach(toast => toast.remove());
        
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <span class="toast-message">${sanitizedMessage}</span>
                <button class="toast-close" aria-label="Close notification">&times;</button>
            </div>
        `;
        
        // Add styles dynamically
        if (!document.querySelector('#toast-styles')) {
            const style = document.createElement('style');
            style.id = 'toast-styles';
            style.textContent = `
                .toast {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background: white;
                    border: 1px solid #e0e0e0;
                    border-radius: 8px;
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
                    z-index: 1000;
                    max-width: 350px;
                    animation: slideIn 0.3s ease;
                }
                
                .toast-info {
                    border-left: 4px solid #7c7cff;
                }
                
                .toast-error {
                    border-left: 4px solid #ff6b6b;
                }
                
                .toast-content {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    padding: 1rem;
                    gap: 1rem;
                }
                
                .toast-message {
                    color: #333;
                    font-size: 0.9rem;
                    line-height: 1.4;
                }
                
                .toast-close {
                    background: none;
                    border: none;
                    font-size: 1.2rem;
                    cursor: pointer;
                    color: #999;
                    padding: 0;
                    width: 20px;
                    height: 20px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }
                
                .toast-close:hover {
                    color: #333;
                }
                
                @keyframes slideIn {
                    from {
                        transform: translateX(100%);
                        opacity: 0;
                    }
                    to {
                        transform: translateX(0);
                        opacity: 1;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Add event listeners
        const closeButton = toast.querySelector('.toast-close');
        closeButton.addEventListener('click', () => toast.remove());
        
        // Auto-remove after 3 seconds
        setTimeout(() => toast.remove(), 3000);
        
        // Add to page
        document.body.appendChild(toast);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new SkyScope();
});

// Handle page visibility changes to refresh if needed
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Re-sync temperature unit when page becomes visible
        const app = window.skyScope;
        if (app) {
            app.currentUnit = app.getCurrentUnit();
        }
    }
});