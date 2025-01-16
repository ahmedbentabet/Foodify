import unittest
from app import app
from flask import json
from models import storage
from models.order import Order
from models.restaurant import Restaurant
from models.review import Review
from flask_login import login_user
from models.user import User


class TestReviewRoutes(unittest.TestCase):
    """Test for review routes"""

    @classmethod
    def setUpClass(cls):
        """Setup before the tests"""
        cls.app = app.test_client()
        cls.app.testing = True

        # Prepare user and orders data for testing
        cls.user = User(id="123", email="testuser@mail.com", password_hash="testpass")
        storage.new(cls.user)
        storage.save()

        cls.restaurant = Restaurant(id="1", name="Pizza Hut", city="Rabat")
        storage.new(cls.restaurant)
        storage.save()

        cls.order = Order(id="1", client_id=cls.user.id, restaurant_id=cls.restaurant.id)
        storage.new(cls.order)
        storage.save()

    def setUp(self):
        """Login before each test"""
        login_user(self.user)

    def test_all_orders_and_review(self):
        """Test the all_orders_and_review route"""
        response = self.app.get('/all_orders_and_review')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Pizza Hut", response.data)  # Checking if restaurant is listed
        self.assertIn(b"Orders", response.data)  # Checking if orders are listed

    def test_submit_review(self):
        """Test submitting a review"""
        data = {
            "restaurant": "Pizza Hut",
            "rating": 4,
            "feedback": "Great food!"
        }

        response = self.app.post('/api/v1/submit_review', 
                                 data=json.dumps(data), 
                                 content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Review submitted successfully", response.data)

    def test_submit_review_missing_fields(self):
        """Test submitting a review with missing fields"""
        data = {
            "restaurant": "Pizza Hut",
            "rating": 4
        }

        response = self.app.post('/api/v1/submit_review', 
                                 data=json.dumps(data), 
                                 content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertIn(b"Missing required fields", response.data)

    def test_submit_review_restaurant_not_found(self):
        """Test submitting a review for a non-existing restaurant"""
        data = {
            "restaurant": "Non-Existing Restaurant",
            "rating": 5,
            "feedback": "Great food!"
        }

        response = self.app.post('/api/v1/submit_review', 
                                 data=json.dumps(data), 
                                 content_type='application/json')

        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Restaurant not found", response.data)

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests"""
        storage.delete(cls.user)
        storage.delete(cls.restaurant)
        storage.delete(cls.order)
        storage.save()


if __name__ == '__main__':
    unittest.main()
