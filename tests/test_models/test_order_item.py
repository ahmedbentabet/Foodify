import unittest
from datetime import datetime
from models.order_item import OrderItem
from models.order import Order
from models.menu_item import MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.base_model import Base


class TestOrderItemModel(unittest.TestCase):
    """Test suite for the OrderItem model"""

    def setUp(self):
        """Set up resources before each test"""
        # Create an in-memory database engine for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)

        # Create a sample Order and MenuItem instances for relationships
        self.order = Order(client_id="test_client_id", status="active", total_price=100.00)
        self.menu_item = MenuItem(restaurant_id="test_restaurant_id", name="Pizza", price=25.00)

        # Add and commit the order and menu item to the session
        self.session.add(self.order)
        self.session.add(self.menu_item)
        self.session.commit()

        # Create a default OrderItem instance
        self.order_item_data = {
            "order_id": self.order.id,
            "menu_item_id": self.menu_item.id,
            "quantity": 2,
        }
        self.order_item = OrderItem(**self.order_item_data)

    def tearDown(self):
        """Clean up resources after each test"""
        # Close the session and remove all data
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_initialization(self):
        """Test the initialization of the OrderItem model"""
        self.assertIsInstance(self.order_item, OrderItem)
        self.assertEqual(self.order_item.order_id, self.order.id)
        self.assertEqual(self.order_item.menu_item_id, self.menu_item.id)
        self.assertEqual(self.order_item.quantity, 2)

    def test_relationship_with_order(self):
        """Test the relationship between OrderItem and Order"""
        self.session.add(self.order_item)
        self.session.commit()

        order_item_from_db = self.session.query(OrderItem).first()
        self.assertEqual(order_item_from_db.order_id, self.order.id)
        self.assertEqual(order_item_from_db.order.status, "active")

    def test_relationship_with_menu_item(self):
        """Test the relationship between OrderItem and MenuItem"""
        self.session.add(self.order_item)
        self.session.commit()

        order_item_from_db = self.session.query(OrderItem).first()
        self.assertEqual(order_item_from_db.menu_item_id, self.menu_item.id)
        self.assertEqual(order_item_from_db.menu_item.name, "Pizza")

    def test_quantity_update(self):
        """Test that the quantity of OrderItem can be updated correctly"""
        self.order_item.quantity = 3
        self.order_item.save()
        self.assertEqual(self.order_item.quantity, 3)

    def test_order_item_total_price(self):
        """Test that the total price of an OrderItem is calculated correctly"""
        total_price = self.order_item.quantity * self.menu_item.price
        self.assertEqual(total_price, 50.00)

if __name__ == "__main__":
    unittest.main()
