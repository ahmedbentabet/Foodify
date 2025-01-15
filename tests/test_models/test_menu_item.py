import unittest
from datetime import datetime
from models.menu_item import MenuItem
from models.restaurant import Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.base_model import Base


class TestMenuItemModel(unittest.TestCase):
    """Test suite for the MenuItem model"""

    def setUp(self):
        """Set up resources before each test"""
        # Create an in-memory database engine for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)

        # Create a restaurant instance for foreign key relationship
        self.restaurant = Restaurant(name="Test Restaurant")
        self.session.add(self.restaurant)
        self.session.commit()

        # Create a default MenuItem instance
        self.menu_item_data = {
            "restaurant_id": self.restaurant.id,
            "name": "Test Dish",
            "price": 10.99,
            "is_available": True,
            "image_url": "http://example.com/image.jpg"
        }
        self.menu_item = MenuItem(**self.menu_item_data)

    def tearDown(self):
        """Clean up resources after each test"""
        # Close the session and remove all data
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_initialization(self):
        """Test the initialization of the MenuItem model"""
        self.assertIsInstance(self.menu_item, MenuItem)
        self.assertEqual(self.menu_item.name, "Test Dish")
        self.assertEqual(self.menu_item.price, 10.99)
        self.assertTrue(self.menu_item.is_available)
        self.assertEqual(self.menu_item.image_url, "http://example.com/image.jpg")
        self.assertEqual(self.menu_item.restaurant_id, self.restaurant.id)

    def test_update(self):
        """Test the update method for MenuItem model"""
        self.menu_item.name = "Updated Dish"
        self.menu_item.price = 12.99
        self.menu_item.is_available = False
        self.menu_item.update(name="Updated Dish", price=12.99, is_available=False)
        self.assertEqual(self.menu_item.name, "Updated Dish")
        self.assertEqual(self.menu_item.price, 12.99)
        self.assertFalse(self.menu_item.is_available)

    def test_relationship_with_restaurant(self):
        """Test the relationship between MenuItem and Restaurant"""
        self.session.add(self.menu_item)
        self.session.commit()

        menu_item_from_db = self.session.query(MenuItem).first()
        self.assertEqual(menu_item_from_db.restaurant.name, "Test Restaurant")
        self.assertEqual(menu_item_from_db.restaurant_id, self.restaurant.id)

    def test_relationship_with_order_items(self):
        """Test the relationship between MenuItem and OrderItem"""
        from models.order_item import OrderItem  # Assuming the OrderItem model exists
        order_item = OrderItem(menu_item_id=self.menu_item.id, quantity=2)
        self.session.add(order_item)
        self.session.commit()

        menu_item_from_db = self.session.query(MenuItem).first()
        self.assertEqual(len(menu_item_from_db.order_items), 1)
        self.assertEqual(menu_item_from_db.order_items[0].quantity, 2)

    def test_availability_toggle(self):
        """Test the toggle functionality for availability"""
        self.menu_item.is_available = False
        self.menu_item.save()
        self.assertFalse(self.menu_item.is_available)

        self.menu_item.is_available = True
        self.menu_item.save()
        self.assertTrue(self.menu_item.is_available)

if __name__ == "__main__":
    unittest.main()
