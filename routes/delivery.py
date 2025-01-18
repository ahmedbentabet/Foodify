from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
from models import storage
from models.client import Client

# Change the blueprint name
delivery_routes = Blueprint('delivery_routes', __name__)  # Changed from location_routes

@delivery_routes.route('/delivery', methods=['GET'])
@login_required
def delivery_page():
    """Render the delivery location page"""
    try:
        with storage.session_scope() as session:
            # Get current client's stored location
            client = session.query(Client).get(current_user.id)
            stored_location = {
                'address': client.address if client.address else None,
                'lat': float(client.latitude) if client.latitude else None,
                'lng': float(client.longitude) if client.longitude else None,
                'contact_name': client.contact_name if client.contact_name else None,
                'phone': client.phone if client.phone else None,
                'instructions': client.delivery_instructions if client.delivery_instructions else None
            }
            return render_template('delivery.html',
                                 stored_location=stored_location,
                                 title='Delivery Details')
    except Exception as e:
        print(f"Error loading delivery page: {e}")
        return render_template('delivery.html',
                             stored_location=None,
                             title='Delivery Details')

@delivery_routes.route('/api/v1/location/save', methods=['POST'])
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
