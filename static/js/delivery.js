// 1. Global Variables
let map, marker, autocomplete;

// 2. Initialize Google Maps (Global Scope)
window.initMap = function() {
    const defaultLocation = { lat: 30.0444, lng: 31.2357 };

    if (!google || !google.maps) {
        showError('Google Maps failed to load');
        return;
    }

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

    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('address-input'),
        { types: ['address'] }
    );

    setupMapFeatures();

    // Try to get user's location initially
    getCurrentLocation();
};

// 3. Main Document Ready Handler
document.addEventListener('DOMContentLoaded', () => {
    // UI Setup
    const elements = {
        locationPrompt: document.getElementById('locationPrompt'),
        mapSection: document.getElementById('mapSection'),
        storedLocationBtn: document.getElementById('useStoredLocation'),
        selectNewLocationBtn: document.getElementById('selectNewLocation')
    };

    // Handle stored location
    if (storedLocation?.lat && storedLocation?.lng && elements.storedLocationBtn) {
        elements.storedLocationBtn.onclick = () => window.location.href = '/payment';
    } else if (elements.mapSection) {
        elements.locationPrompt.style.display = 'none';
        elements.mapSection.style.display = 'block';
    }

    // Setup form handling
    const deliveryForm = document.getElementById('delivery-form');
    if (deliveryForm) {
        deliveryForm.addEventListener('submit', handleFormSubmission);
    }

    // Setup phone validation
    const phoneInput = document.getElementById('phone');
    if (phoneInput) {
        phoneInput.addEventListener('input', (e) => {
            phoneInput.style.borderColor = validatePhone(e.target.value) ? '#ccc' : 'red';
        });
    }

    // Setup geolocation button
    document.getElementById('geolocateMe')?.addEventListener('click', handleGeolocation);
});

// 4. Helper Functions
function setupMapFeatures() {
    autocomplete.bindTo('bounds', map);

    map.addListener('click', (e) => {
        placeMarker(e.latLng);
        getAddressFromLatLng(e.latLng);
    });

    autocomplete.addListener('place_changed', () => {
        const place = autocomplete.getPlace();
        if (place.geometry) {
            map.setCenter(place.geometry.location);
            placeMarker(place.geometry.location);
            map.setZoom(17);
        }
    });
}

async function handleFormSubmission(e) {
    e.preventDefault();

    const formData = {
        contactName: document.getElementById('contact-name').value,
        phone: document.getElementById('phone').value,
        address: document.getElementById('address-input').value,
        instructions: document.getElementById('instructions').value
    };

    if (!validateFormData(formData)) return;

    try {
        const response = await saveLocation(formData);
        if (response.ok) {
            showSuccess('Location saved successfully!');
            window.location.href = '/payment';
        }
    } catch (error) {
        showError(error.message);
    }
}

// 5. Utility Functions
function validateFormData(data) {
    if (!marker) {
        showError('Please select a delivery location on the map');
        return false;
    }
    if (!data.contactName) {
        showError('Please enter a contact name');
        return false;
    }
    if (!data.phone) {
        showError('Please enter a phone number');
        return false;
    }
    if (!validatePhone(data.phone)) {
        showError('Please enter a valid phone number (minimum 10 digits)');
        return false;
    }
    if (!data.address) {
        showError('Please enter a delivery address');
        return false;
    }
    return true;
}

function validatePhone(phone) {
    return /^\+?[\d\s-]{10,}$/.test(phone);
}

function showError(message) {
    showNotification(message, 'error-message');
}

function showSuccess(message) {
    showNotification(message, 'success-message');
}

function showNotification(message, className) {
    // Remove any existing notifications
    const existingNotifications = document.querySelectorAll('.error-message, .success-message');
    existingNotifications.forEach(notification => notification.remove());

    // Create new notification
    const div = document.createElement('div');
    div.className = className;

    // Add icon based on message type
    const icon = className.includes('error') ? '⚠️' : '✅';
    div.innerHTML = `${icon} ${message}`;

    // Add to DOM
    document.querySelector('.delivery-container').prepend(div);

    // Remove after delay
    setTimeout(() => {
        div.style.opacity = '0';
        setTimeout(() => div.remove(), 500);
    }, 5000);
}

function placeMarker(location) {
    if (marker) marker.setMap(null);
    marker = new google.maps.Marker({
        position: location,
        map: map,
        animation: google.maps.Animation.DROP,
        title: 'Delivery Location'
    });
}

function getAddressFromLatLng(latLng) {
    const geocoder = new google.maps.Geocoder();
    geocoder.geocode({ location: latLng }, (results, status) => {
        if (status === 'OK' && results[0]) {
            document.getElementById('address-input').value = results[0].formatted_address;
        } else {
            showError('Could not get address from this location');
        }
    });
}

function handleGeolocation() {
    if (!navigator.geolocation) {
        showError('Geolocation is not supported by your browser');
        return;
    }

    showNotification('Getting your location...', 'success-message');

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
            placeMarker(pos);
            getAddressFromLatLng(pos);
            showSuccess('Location found successfully!');
        },
        (error) => {
            let errorMessage;
            switch(error.code) {
                case error.PERMISSION_DENIED:
                    errorMessage = "Location access denied. Please enable location services in your browser.";
                    break;
                case error.POSITION_UNAVAILABLE:
                    errorMessage = "Unable to detect your location. Please try again.";
                    break;
                case error.TIMEOUT:
                    errorMessage = "Location request timed out. Please check your connection.";
                    break;
                default:
                    errorMessage = "An unexpected error occurred while getting your location.";
            }
            showError(errorMessage);
        },
        {
            timeout: 10000,
            enableHighAccuracy: true
        }
    );
}

function getCurrentLocation() {
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
            () => {
                // Silently fail and use default location
                console.log("Geolocation failed, using default location");
            }
        );
    }
}

async function saveLocation(formData) {
    try {
        if (!marker) {
            throw new Error('Please select a location on the map');
        }

        const response = await fetch('/api/v1/location/save', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                lat: marker.getPosition().lat(),
                lng: marker.getPosition().lng(),
                address: formData.address,
                instructions: formData.instructions,
                contact_name: formData.contactName,
                phone: formData.phone
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to save location');
        }

        return response;
    } catch (error) {
        showError(`Error: ${error.message}`);
        throw error;
    }
}

// ...existing error handling and utility functions remain unchanged...