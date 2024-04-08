document.getElementById('weatherForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var city = document.getElementById('city').value;
    fetch('/weather?city=' + city)
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            // Vulnerable code: Directly using user-provided data to manipulate the DOM
            document.getElementById('weatherInfo').innerHTML = 'Weather in ' + city + ': ' + data.weather;
        })
        .catch(function(error) {
            console.error('Error:', error);
        });
});

document.getElementById('executeCode').addEventListener('click', function(event) {
    event.preventDefault();
    var code = document.getElementById('code').value;

    // Vulnerable code: Directly using user-provided data in eval function
    eval(code);
});