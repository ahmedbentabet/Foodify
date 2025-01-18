from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import storage
from models.client import Client

location_routes = Blueprint('location_routes', __name__)


@location_routes.route('/api/v1/location/save', methods=['POST'])
@login_required
def save_location():
    """Save delivery location and contact information"""
    try:
        with storage.session_scope() as session:
            data = request.get_json()

            # Validate required fields
            required_fields = ['lat', 'lng', 'address', 'contact_name', 'phone']
            if not all(field in data for field in required_fields):
                return jsonify({
                    'error': 'Missing required fields'
                }), 400

            # Get current client
            client = session.query(Client).get(current_user.id)
            if not client:
                return jsonify({'error': 'Client not found'}), 404

            # Update client information
            client.address = data['address']
            client.latitude = data['lat']
            client.longitude = data['lng']
            client.phone = data['phone']
            client.delivery_instructions = data.get('instructions', '')
            client.contact_name = data['contact_name']

            # Commit changes
            session.commit()

            return jsonify({
                'success': True,
                'message': 'Location saved successfully'
            }), 200

    except Exception as e:
        print(f"Error saving location: {e}")
        return jsonify({'error': str(e)}), 500
