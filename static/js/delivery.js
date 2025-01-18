let map;
let marker;
let autocomplete;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize location handling
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

    // Initialize Google Maps
    function initializeMap() {
        const defaultLocation = { lat: 30.0444, lng: 31.2357 }; // Cairo coordinates as default

        map = new google.maps.Map(document.getElementById('map'), {
            zoom: 15,
            center: defaultLocation,
            styles: [
                {
                    "featureType": "poi",
                    "elementType": "labels",
                    "stylers": [{ "visibility": "off" }]
                },
                {
                    "featureType": "transit",
                    "elementType": "labels",
                    "stylers": [{ "visibility": "off" }]
                }
            ],
            mapTypeControl: false,
            fullscreenControl: false,
            streetViewControl: false
        });

        // Initialize Places Autocomplete
        autocomplete = new google.maps.places.Autocomplete(
            document.getElementById('address-input'),
            { types: ['address'] }
        );

        // Bias autocomplete results to map's current viewport
        autocomplete.bindTo('bounds', map);

        // Add marker on map click
        map.addListener('click', (e) => {
            placeMarker(e.latLng);
            getAddressFromLatLng(e.latLng);
        });

        // Update map when place is selected
        autocomplete.addListener('place_changed', () => {
            const place = autocomplete.getPlace();
            if (place.geometry) {
                map.setCenter(place.geometry.location);
                placeMarker(place.geometry.location);
                map.setZoom(17);
            }
        });

        // Try to get user's current location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    map.setCenter(pos);
                    placeMarker(pos);
                    getAddressFromLatLng(pos);
                },
                (error) => {
                    handleLocationError(error);
                }
            );
        }
    }

    // Get address from coordinates
    function getAddressFromLatLng(latLng) {
        const geocoder = new google.maps.Geocoder();
        geocoder.geocode({ location: latLng }, (results, status) => {
            if (status === 'OK') {
                if (results[0]) {
                    document.getElementById('address-input').value = results[0].formatted_address;
                }
            } else {
                showError('Could not get address from this location');
            }
        });
    }

    // Handle geolocation
    document.getElementById('geolocateMe').addEventListener('click', () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    };
                    map.setCenter(pos);
                    placeMarker(pos);
                },
                (error) => {
                    handleLocationError(error);
                }
            );
        } else {
            showError('Geolocation is not supported by your browser.');
        }
    });

    // Place marker on map
    function placeMarker(location) {
        if (marker) {
            marker.setMap(null);
        }
        marker = new google.maps.Marker({
            position: location,
            map: map,
            animation: google.maps.Animation.DROP,
            draggable: true
        });

        // Update address when marker is dragged
        marker.addListener('dragend', () => {
            getAddressFromLatLng(marker.getPosition());
        });
    }

    // Handle form submission
    document.getElementById('delivery-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!marker) {
            showError('Please select a delivery location');
            return;
        }

        try {
            const response = await fetch('/api/v1/location/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lat: marker.getPosition().lat(),
                    lng: marker.getPosition().lng(),
                    address: document.getElementById('address-input').value,
                    instructions: document.getElementById('instructions').value,
                    contact_name: document.getElementById('contact-name').value,
                    phone: document.getElementById('phone').value
                })
            });

            if (!response.ok) {
                throw new Error('Failed to save location');
            }

            window.location.href = '/payment';
        } catch (error) {
            showError(error.message);
        }
    });

    // Error handling
    function handleLocationError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                showError("Please allow location access to use this feature");
                break;
            case error.POSITION_UNAVAILABLE:
                showError("Location information is unavailable");
                break;
            case error.TIMEOUT:
                showError("Location request timed out");
                break;
            default:
                showError("An unknown error occurred");
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
});