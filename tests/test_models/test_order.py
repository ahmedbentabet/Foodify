import unittest
from datetime import datetime
from models.order import Order
from models.client import Client
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.base_model import Base


class TestOrderModel(unittest.TestCase):
    """Test suite for the Order model"""

    def setUp(self):
        """Set up resources before each test"""
        # Create an in-memory database engine for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)

        # Create a client instance for foreign key relationship
        self.client = Client(username="testuser", email="test@example.com", password="password")
        self.session.add(self.client)
        self.session.commit()

        # Create a default Order instance
        self.order_data = {
            "client_id": self.client.id,
            "status": "active",
            "total_price": 100.00,
        }
        self.order = Order(**self.order_data)

    def tearDown(self):
        """Clean up resources after each test"""
        # Close the session and remove all data
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_initialization(self):
        """Test the initialization of the Order model"""
        self.assertIsInstance(self.order, Order)
        self.assertEqual(self.order.status, "active")
        self.assertEqual(self.order.total_price, 100.00)
        self.assertEqual(self.order.client_id, self.client.id)
        self.assertIsInstance(self.order.order_date, datetime)

    def test_update_status(self):
        """Test updating the status of the Order"""
        self.order.status = "completed"
        self.order.save()
        self.assertEqual(self.order.status, "completed")

    def test_relationship_with_client(self):
        """Test the relationship between Order and Client"""
        self.session.add(self.order)
        self.session.commit()

        order_from_db = self.session.query(Order).first()
        self.assertEqual(order_from_db.client.username, "testuser")
        self.assertEqual(order_from_db.client_id, self.client.id)

    def test_relationship_with_order_items(self):
        """Test the relationship between Order and OrderItem"""
        from models.order_item import OrderItem  # Assuming OrderItem exists
        order_item = OrderItem(order_id=self.order.id, menu_item_id="some_id", quantity=2)
        self.session.add(order_item)
        self.session.commit()

        order_from_db = self.session.query(Order).first()
        self.assertEqual(len(order_from_db.order_items), 1)
        self.assertEqual(order_from_db.order_items[0].quantity, 2)

    def test_order_total_price_calculation(self):
        """Test that the total_price is set correctly"""
        order_item_data = {
            "menu_item_id": "some_item_id",
            "order_id": self.order.id,
            "quantity": 2,
            "price": 25.00
        }
        # Assuming we have an OrderItem class to calculate total price
        from models.order_item import OrderItem
        order_item = OrderItem(**order_item_data)
        self.session.add(order_item)
        self.session.commit()

        self.order.total_price = sum(item.price * item.quantity for item in self.order.order_items)
        self.assertEqual(self.order.total_price, 50.00)

if __name__ == "__main__":
    unittest.main()
