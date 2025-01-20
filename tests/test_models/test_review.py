import unittest
from models.review import Review
from models.client import Client
from models.restaurant import Restaurant
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models.base_model import Base


class TestReviewModel(unittest.TestCase):
    """Test suite for the Review model"""

    def setUp(self):
        """Set up resources before each test"""
        # Create an in-memory database engine for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)

        # Create a new session for each test
        self.session = Session(self.engine)

        # Create sample Client and Restaurant instances
        self.client = Client(id="client1", username="john_doe", email="john@example.com", password="password")
        self.restaurant = Restaurant(id="restaurant1", name="Pizza Palace", city="New York")

        # Add them to the session and commit
        self.session.add(self.client)
        self.session.add(self.restaurant)
        self.session.commit()

        # Create a sample Review instance
        self.review_data = {
            "client_id": self.client.id,
            "restaurant_id": self.restaurant.id,
            "rating": 5,
            "comment": "Great food and service!",
        }
        self.review = Review(**self.review_data)

    def tearDown(self):
        """Clean up resources after each test"""
        # Close the session and remove all data
        self.session.close()
        Base.metadata.drop_all(self.engine)

    def test_initialization(self):
        """Test the initialization of the Review model"""
        self.assertIsInstance(self.review, Review)
        self.assertEqual(self.review.client_id, self.client.id)
        self.assertEqual(self.review.restaurant_id, self.restaurant.id)
        self.assertEqual(self.review.rating, 5)
        self.assertEqual(self.review.comment, "Great food and service!")

    def test_relationship_with_client(self):
        """Test the relationship between Review and Client"""
        self.session.add(self.review)
        self.session.commit()

        review_from_db = self.session.query(Review).first()
        self.assertEqual(review_from_db.client.username, "john_doe")

    def test_relationship_with_restaurant(self):
        """Test the relationship between Review and Restaurant"""
        self.session.add(self.review)
        self.session.commit()

        review_from_db = self.session.query(Review).first()
        self.assertEqual(review_from_db.restaurant.name, "Pizza Palace")

    def test_missing_comment(self):
        """Test the behavior when no comment is provided"""
        review_without_comment = Review(
            client_id=self.client.id, 
            restaurant_id=self.restaurant.id, 
            rating=4
        )
        self.assertIsNone(review_without_comment.comment)

    def test_invalid_rating(self):
        """Test invalid rating value"""
        with self.assertRaises(ValueError):
            Review(client_id=self.client.id, restaurant_id=self.restaurant.id, rating=11)

    def test_negative_rating(self):
        """Test negative rating value"""
        with self.assertRaises(ValueError):
            Review(client_id=self.client.id, restaurant_id=self.restaurant.id, rating=-1)

if __name__ == "__main__":
    unittest.main()
