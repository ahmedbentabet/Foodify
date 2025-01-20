import unittest
from flask import Flask
from flask_testing import TestCase
from app import create_app
from models import storage
from models.menu_item import MenuItem
from models.restaurant import Restaurant
from flask import jsonify


class TestWelcomeRoutes(TestCase):
    def create_app(self):
        app = create_app("testing")  # Use testing configuration
        return app

    def setUp(self):
        """Sets up the test environment before each test"""
        with self.create_app().app_context():
            storage.clear()  # Clear the database before each test

            # Create test restaurant and menu items
            restaurant = Restaurant(name="Test Restaurant")
            storage.new(restaurant)
            storage.save()

            menu_item1 = MenuItem(
                name="Test Meal 1",
                price=12.99,
                restaurant=restaurant,
                is_available=True,
            )
            menu_item2 = MenuItem(
                name="Test Meal 2",
                price=15.49,
                restaurant=restaurant,
                is_available=True,
            )
            storage.new(menu_item1)
            storage.new(menu_item2)
            storage.save()

    def tearDown(self):
        """Clears after each test"""
        with self.create_app().app_context():
            storage.clear()

    def test_welcome_page(self):
        """Test the welcome route renders correctly"""
        response = self.client.get("/welcome")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome to Foodify", response.data)

    def test_search_meals_no_filter(self):
        """Test search meals without filters"""
        response = self.client.get("/api/v1/search")
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data["meals"]), 2)  # Should return 2 menu items
        self.assertEqual(data["total"], 2)

    def test_search_meals_with_query(self):
        """Test search meals with query filter"""
        response = self.client.get("/api/v1/search", query_string={"query": "Test Meal 1"})
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data["meals"]), 1)  # Should return 1 menu item
        self.assertEqual(data["total"], 1)
        self.assertEqual(data["meals"][0]["name"], "Test Meal 1")

    def test_search_meals_with_pagination(self):
        """Test search meals with pagination"""
        response = self.client.get("/api/v1/search", query_string={"page": 2})
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data["meals"]), 0)  # Since we only have 2 meals, page 2 should return no results
        self.assertEqual(data["total"], 2)

    def test_search_meals_with_restaurant_filter(self):
        """Test search meals with restaurant filter"""
        response = self.client.get("/api/v1/search", query_string={"restaurant": "Test Restaurant"})
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data["meals"]), 2)  # Should return meals from the "Test Restaurant"
        self.assertEqual(data["total"], 2)

    def test_search_meals_with_no_results(self):
        """Test search meals with no matching results"""
        response = self.client.get("/api/v1/search", query_string={"query": "Nonexistent Meal"})
        self.assertEqual(response.status_code, 200)

        data = response.json
        self.assertEqual(len(data["meals"]), 0)  # No meals should match
        self.assertEqual(data["total"], 0)


if __name__ == "__main__":
    unittest.main()
