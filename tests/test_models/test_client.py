import unittest
from unittest.mock import patch
from datetime import datetime
from models.client import Client
from models.base_model import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


class TestClientModel(unittest.TestCase):
    """Test suite for the Client model"""

    def setUp(self):
        """Set up resources before each test"""
        # Create an in-memory database engine for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)

        # Create a default Client instance
        self.client_data = {
            "username": "test_user",
            "address": "1234 Test Address",
            "email": "test_user@example.com",
            "password": "hashedpassword123"
        }
        self.client = Client(**self.client_data)

    def tearDown(self):
        """Clean up resources after each test"""
        # Close the session and remove all data
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_initialization(self):
        """Test the initialization of the Client model"""
        self.assertIsInstance(self.client, Client)
        self.assertEqual(self.client.username, "test_user")
        self.assertEqual(self.client.address, "1234 Test Address")
        self.assertEqual(self.client.email, "test_user@example.com")
        self.assertEqual(self.client.password, "hashedpassword123")

    def test_update(self):
        """Test the update method for Client model"""
        self.client.update(email="new_email@example.com", address="New Address")
        self.assertEqual(self.client.email, "new_email@example.com")
        self.assertEqual(self.client.address, "New Address")

        # Ensure that non-allowed fields are not updated
        self.client.update(username="new_username")  # username is not allowed
        self.assertEqual(self.client.username, "test_user")

    def test_invalid_update(self):
        """Test the update method when invalid fields are provided"""
        initial_email = self.client.email
        initial_address = self.client.address
        self.client.update(invalid_field="invalid_value")
        self.assertEqual(self.client.email, initial_email)
        self.assertEqual(self.client.address, initial_address)

    def test_relationship_with_reviews(self):
        """Test the relationship between Client and Review"""
        # Create a new review associated with the client
        from models.review import Review  # Assuming the Review model exists
        review = Review(content="Great service!", client_id=self.client.id)

        self.session.add(review)
        self.session.commit()

        # Fetch the client from the database and verify the relationship
        client_from_db = self.session.query(Client).first()
        self.assertEqual(len(client_from_db.reviews), 1)
        self.assertEqual(client_from_db.reviews[0].content, "Great service!")

    def test_relationship_with_orders(self):
        """Test the relationship between Client and Order"""
        # Create a new order associated with the client
        from models.order import Order  # Assuming the Order model exists
        order = Order(order_details="Order 1", client_id=self.client.id)

        self.session.add(order)
        self.session.commit()

        # Fetch the client from the database and verify the relationship
        client_from_db = self.session.query(Client).first()
        self.assertEqual(len(client_from_db.orders), 1)
        self.assertEqual(client_from_db.orders[0].order_details, "Order 1")

if __name__ == "__main__":
    unittest.main()
