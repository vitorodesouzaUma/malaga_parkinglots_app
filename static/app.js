var mapInitialized = false;

        function updateData() {
            if(!mapInitialized){
                fetch('/map')
                    .then(response => response.json())
                    .then(data => {
                        if (!mapInitialized) {
                            var map = L.map('map').setView([36.7132139, -4.4076681], 13);

                            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                                attribution: '© OpenStreetMap contributors'
                            }).addTo(map);

                            mapInitialized = true;
                        }

                        var parkingData = data;

                        if (parkingData && Array.isArray(parkingData) && parkingData.length > 0) {
                            for (var i = 0; i < parkingData.length; i++) {
                                if (parkingData[i].availableSpotNumber.value>0){
                                    var latitude = parkingData[i].location.value.coordinates[1];
                                    var longitude = parkingData[i].location.value.coordinates[0];
                                    var spotNumber = parkingData[i].availableSpotNumber.value;
                                    var name = parkingData[i].name?.value;

                                    if (latitude !== undefined && longitude !== undefined && spotNumber !== undefined && name !== undefined) {
                                        L.marker([latitude, longitude]).addTo(map).bindPopup(name + ": " + spotNumber + " spots available");

                                        var table = document.getElementById("parking-table");
                                        var row = table.insertRow(i + 1);
                                        var cell1 = row.insertCell(0);
                                        var cell2 = row.insertCell(1);
                                        var cell3 = row.insertCell(2);

                                        cell1.innerHTML = name;
                                        cell2.innerHTML = spotNumber;
                                        cell3.innerHTML = parkingData[i].status?.value[0] || "N/A";
                                    }
                                }
                            }
                        } else {
                            console.log("No valid parking data received.");
                        }
                    })
                    .catch(error => {
                        console.error("Error fetching parking data:", error);
                    });
            }
        }

        // Initial update on page load
        updateData();

        // Schedule updates every minute
        setInterval(updateData, 60000);