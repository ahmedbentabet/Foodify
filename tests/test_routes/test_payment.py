import unittest
from flask import Flask
from flask_testing import TestCase
from models import storage
from models.order import Order
from models.menu_item import MenuItem
from flask_login import login_user
from your_app import app  # Replace with your actual app import
from flask_login import UserMixin


class TestPaymentRoutes(TestCase):
    def create_app(self):
        # Set up the app with a test configuration
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for testing
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        """Set up a test client and create a test user"""
        self.client = self.app.test_client()

        # Create a user for login (replace with your actual user model)
        self.test_user = self.create_test_user()

        # Log in the test user
        login_user(self.test_user)

    def create_test_user(self):
        """Create a mock user for testing purposes"""
        # Replace with actual user creation logic (e.g., using UserMixin)
        from models.client import Client
        user = Client(email="testuser@example.com", password="password123")
        storage.new(user)
        storage.save()
        return user

    def test_payment_route(self):
        """Test payment page rendering"""
        # Create an active order for the test user
        order = Order(client_id=self.test_user.id, status="active", total_price=20.00)
        storage.new(order)
        storage.save()

        # Add items to the order
        menu_item = MenuItem(name="Pizza", price=10.00)
        storage.new(menu_item)
        storage.save()

        order_item = order.add_item(menu_item.id, 2)  # Add two pizzas to the order
        storage.save()

        # Visit the payment page
        response = self.client.get('/payment')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"payment.html", response.data)
        self.assertIn(b"Pizza", response.data)
        self.assertIn(b"20.00", response.data)  # Check if subtotal is correct

    def test_get_totals_route(self):
        """Test getting the order totals for AJAX"""
        # Create an active order for the test user
        order = Order(client_id=self.test_user.id, status="active", total_price=20.00)
        storage.new(order)
        storage.save()

        # Add items to the order
        menu_item = MenuItem(name="Pizza", price=10.00)
        storage.new(menu_item)
        storage.save()

        order_item = order.add_item(menu_item.id, 2)  # Add two pizzas to the order
        storage.save()

        # Test the /api/v1/payment/totals route for AJAX response
        response = self.client.get('/api/v1/payment/totals')
        self.assertEqual(response.status_code, 200)
        json_response = response.get_json()
        self.assertTrue(json_response['success'])
        self.assertEqual(json_response['subtotal'], '20.00')
        self.assertEqual(json_response['delivery_fee'], '5.00')
        self.assertEqual(json_response['total'], '25.00')

    def tearDown(self):
        """Clean up after each test"""
        storage.rollback()


if __name__ == '__main__':
    unittest.main()
