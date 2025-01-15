import unittest
from models.restaurant import Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.base_model import Base


class TestRestaurantModel(unittest.TestCase):
    """Test suite for the Restaurant model"""

    def setUp(self):
        """Set up resources before each test"""
        # Create an in-memory database engine for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)

        # Create a sample Restaurant instance
        self.restaurant_data = {
            "name": "Pizza Palace",
            "city": "New York",
            "logo_url": "http://example.com/logo.png",
        }
        self.restaurant = Restaurant(**self.restaurant_data)

    def tearDown(self):
        """Clean up resources after each test"""
        # Close the session and remove all data
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_initialization(self):
        """Test the initialization of the Restaurant model"""
        self.assertIsInstance(self.restaurant, Restaurant)
        self.assertEqual(self.restaurant.name, "Pizza Palace")
        self.assertEqual(self.restaurant.city, "New York")
        self.assertEqual(self.restaurant.logo_url, "http://example.com/logo.png")

    def test_relationship_with_reviews(self):
        """Test the relationship between Restaurant and Review"""
        # Add the restaurant to the session and commit
        self.session.add(self.restaurant)
        self.session.commit()

        # Check the relationship with reviews
        restaurant_from_db = self.session.query(Restaurant).first()
        self.assertEqual(len(restaurant_from_db.reviews), 0)

    def test_relationship_with_menu_items(self):
        """Test the relationship between Restaurant and MenuItem"""
        # Add the restaurant to the session and commit
        self.session.add(self.restaurant)
        self.session.commit()

        # Check the relationship with menu items
        restaurant_from_db = self.session.query(Restaurant).first()
        self.assertEqual(len(restaurant_from_db.menu_items), 0)

    def test_missing_logo_url(self):
        """Test the restaurant initialization without logo_url"""
        restaurant_without_logo = Restaurant(name="Burger King", city="Los Angeles")
        self.assertIsNone(restaurant_without_logo.logo_url)

if __name__ == "__main__":
    unittest.main()
