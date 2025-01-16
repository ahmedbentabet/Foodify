import unittest
from flask import Flask, jsonify
from flask_testing import TestCase
from flask_login import LoginManager, UserMixin, login_user
from app import app, storage
from models import Client, Order, MenuItem, OrderItem
from unittest.mock import patch

class OrderRoutesTestCase(TestCase):
    """Test cases for Order Routes"""

    def create_app(self):
        """Setup Flask app for testing"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory DB for testing
        login_manager = LoginManager()
        login_manager.init_app(app)
        return app

    def setUp(self):
        """Set up the test environment"""
        # Create a test user and log them in
        self.client = Client(email='test@example.com', password='testpassword')
        self.client.set_password('testpassword')
        storage.new(self.client)
        storage.save()

        # Create a test menu item
        self.menu_item = MenuItem(name="Test Dish", price=10.0)
        storage.new(self.menu_item)
        storage.save()

        # Create an active order for the test user
        self.active_order = Order(client_id=self.client.id, status="active", total_price=0.0)
        storage.new(self.active_order)
        storage.save()

        # Log in as the test user
        with self.client as c:
            login_user(self.client)

    def tearDown(self):
        """Clean up after tests"""
        # Clear the storage and any other clean-up
        storage.rollback()

    @patch('models.storage.session_scope')
    def test_update_cart_increase_item(self, mock_session_scope):
        """Test adding an item to the cart"""
        with mock_session_scope as mock_session:
            response = self.client.post(
                '/api/v1/cart/update',
                json={'menu_item_id': self.menu_item.id, 'action': 'increase'}
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn('success', response.json)
            self.assertEqual(response.json['item']['quantity'], 1)

    @patch('models.storage.session_scope')
    def test_update_cart_decrease_item(self, mock_session_scope):
        """Test decreasing an item quantity in the cart"""
        # Add an item first
        self.client.post(
            '/api/v1/cart/update',
            json={'menu_item_id': self.menu_item.id, 'action': 'increase'}
        )

        # Now decrease the item
        response = self.client.post(
            '/api/v1/cart/update',
            json={'menu_item_id': self.menu_item.id, 'action': 'decrease'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json)
        self.assertEqual(response.json['item']['quantity'], 0)

    @patch('models.storage.session_scope')
    def test_get_cart_state(self, mock_session_scope):
        """Test getting the current cart state"""
        response = self.client.get('/api/v1/cart/state')
        self.assertEqual(response.status_code, 200)
        self.assertIn('items', response.json)
        self.assertIn('order', response.json)
        self.assertEqual(response.json['order']['id'], self.active_order.id)

    @patch('models.storage.session_scope')
    def test_confirm_order(self, mock_session_scope):
        """Test confirming the order"""
        response = self.client.post(
            '/confirm_order',
            json={'payment_method': 'credit_card'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn('success', response.json)
        self.assertEqual(response.json['message'], 'Order confirmed successfully')

    @patch('models.storage.session_scope')
    def test_confirm_order_no_active(self, mock_session_scope):
        """Test confirming order when there is no active order"""
        # Remove the active order to simulate no active order
        self.active_order.status = 'completed'
        storage.save()

        response = self.client.post(
            '/confirm_order',
            json={'payment_method': 'credit_card'}
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)
        self.assertEqual(response.json['error'], 'No active order found')


if __name__ == '__main__':
    unittest.main()
