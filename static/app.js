$(document).ready(function () {
    // Load parking lot data from the backend
    $.get('/api/parking-lots', function (data) {
        // Create a Leaflet map
        var map = L.map('map').setView([36.7194, -4.4200], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Populate the parking lots table and add markers to the map
        data.forEach(function (lot) {
            $('#parking-lots-table tbody').append(`
                <tr>
                    <td>${lot.name}</td>
                    <td>${lot.usage}%</td>
                </tr>
            `);

            L.marker([lot.lat, lot.lon]).addTo(map)
                .bindPopup(`<b>${lot.name}</b><br>Usage: ${lot.usage}%`);
        });
    });
});
