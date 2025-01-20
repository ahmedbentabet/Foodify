// Initialize globals
let map;
let marker;
let searchBox;

// TomTom API key
const API_KEY = "gTnO8GY8uqFMsvsF9yz3wZdxMFWBR0kJ";

document.addEventListener('DOMContentLoaded', () => {
    const locationPrompt = document.getElementById('locationPrompt');
    const mapSection = document.getElementById('mapSection');

    // Handle stored location choice
    document.getElementById('useStoredLocation').addEventListener('click', () => {
        window.location.href = '/payment';
    });

    document.getElementById('selectNewLocation').addEventListener('click', () => {
        locationPrompt.style.display = 'none';
        mapSection.style.display = 'block';
        initializeMap();
    });

    // Initialize map
    function initializeMap() {
        map = tt.map({
            key: API_KEY,
            container: 'map',
            center: [31.2357, 30.0444], // Cairo coordinates
            zoom: 13
        });

        // Add search box
        const searchBoxService = new tt.services.fuzzySearch({
            key: API_KEY
        });

        const searchBoxElement = document.getElementById('searchInput');
        searchBox = new tt.plugins.SearchBox(searchBoxService, {
            showSearchButton: false,
            searchBoxHTML: searchBoxElement.outerHTML
        });
        searchBoxElement.parentNode.replaceChild(searchBox.getSearchBoxHTML(), searchBoxElement);

        // Handle search results
        searchBox.on('tomtom.searchbox.resultselected', function(event) {
            const coords = event.data.result.position;
            placeMarker([coords.lng, coords.lat]);
            getAddress(coords);
        });

        // Add marker on map click
        map.on('click', (e) => {
            placeMarker(e.lngLat);
            getAddress(e.lngLat);
        });
    }

    // Handle geolocation
    document.getElementById('geolocateMe').addEventListener('click', () => {
        if (!navigator.geolocation) {
            showError('Geolocation is not supported by your browser');
            return;
        }

        navigator.geolocation.getCurrentPosition(
            position => {
                const coords = {
                    lng: position.coords.longitude,
                    lat: position.coords.latitude
                };
                map.flyTo({
                    center: [coords.lng, coords.lat],
                    zoom: 15
                });
                placeMarker([coords.lng, coords.lat]);
                getAddress(coords);
            },
            error => {
                handleLocationError(error);
            }
        );
    });

    // Form submission
    document.getElementById('locationForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!marker) {
            showError('Please select a location on the map');
            return;
        }

        try {
            const response = await fetch('/api/v1/location/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lat: marker.getLngLat().lat,
                    lng: marker.getLngLat().lng,
                    address: document.getElementById('address').value,
                    instructions: document.getElementById('instructions').value
                })
            });

            if (response.ok) {
                window.location.href = '/payment';
            } else {
                throw new Error('Failed to save location');
            }
        } catch (error) {
            showError(error.message);
        }
    });
});

function placeMarker(lngLat) {
    if (marker) marker.remove();
    marker = new tt.Marker()
        .setLngLat(lngLat)
        .addTo(map);
}

function getAddress(coords) {
    tt.services.reverseGeocode({
        key: API_KEY,
        position: coords
    })
    .then(response => {
        if (response.addresses && response.addresses.length > 0) {
            document.getElementById('address').value = response.addresses[0].address.freeformAddress;
        }
    })
    .catch(error => {
        showError('Could not fetch address');
        console.error(error);
    });
}

function handleLocationError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            showError('Please allow location access to use this feature');
            break;
        case error.POSITION_UNAVAILABLE:
            showError('Location information unavailable');
            break;
        case error.TIMEOUT:
            showError('Location request timed out');
            break;
        default:
            showError('An unknown error occurred');
            break;
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    document.querySelector('.delivery-container').prepend(errorDiv);
    setTimeout(() => errorDiv.remove(), 5000);
}