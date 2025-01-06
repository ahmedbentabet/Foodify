#!/usr/bin/env python3
"""Signup route handler"""
from flask import jsonify, request
from werkzeug.security import generate_password_hash
from Foodify.models.client import Client
from models import storage
from web_flask import app
import re


@app.route('/signup', methods=['POST'])
def signup():
    """Handle user signup"""

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing {field}'}), 400

    # Validate email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, data['email']):
        return jsonify({'error': 'Invalid email format'}), 400

    # Validate password length
    if len(data['password']) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    # Check if email already exists
    all_clients = storage.all(Client)
    if any(client.email == data['email'] for client in all_clients.values()):
        return jsonify({'error': 'Email already exists'}), 400

    # Create new client
    hashed_password = generate_password_hash(data['password'])
    new_client = Client(
        username=data['username'],
        email=data['email'],
        password_hash=hashed_password
    )
    
    # Save to database
    storage.new(new_client)
    storage.save()
    
    # Return success response without password hash
    return jsonify({
        'status': 'success',
        'message': 'User created successfully',
        'data': {
            'id': new_client.id,
            'username': new_client.username,
            'email': new_client.email
        }
    }), 201

