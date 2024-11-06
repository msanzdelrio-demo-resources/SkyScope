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