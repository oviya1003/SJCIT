// Form submission
document.getElementById('locationForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Show spinner when fetch starts
    document.getElementById('spinner').classList.remove('hidden');

    // Use the Geolocation API to get the user's current position
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;

            // Hide spinner when fetch ends
            document.getElementById('spinner').classList.add('hidden');

            // Show map and update with the current location
            document.getElementById('mapContainer').classList.remove('hidden');
            var map = L.map('map').setView([lat, lon], 13);

            // Add OpenStreetMap tile layer
            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; OpenStreetMap contributors',
            }).addTo(map);

            // Add marker to the map
            L.marker([lat, lon]).addTo(map)
                .bindPopup(`Current Location`)
                .openPopup();

        }, function (error) {
            // Handle error if geolocation fails
            document.getElementById('spinner').classList.add('hidden');
            console.error('Error:', error);
            alert('Unable to retrieve your location. Please enable location services.');
        });
    } else {
        // Geolocation not supported
        document.getElementById('spinner').classList.add('hidden');
        alert('Geolocation is not supported by your browser.');
    }
});



