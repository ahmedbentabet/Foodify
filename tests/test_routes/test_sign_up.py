import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import current_user
from app import create_app
from models import storage
from models.client import Client
from werkzeug.security import check_password_hash

class TestSignUpRoute(TestCase):
    def create_app(self):
        app = create_app("testing")  # Use testing configuration
        return app

    def setUp(self):
        """Sets up the test environment before each test"""
        # Create a new app context and session for the test
        with self.create_app().app_context():
            storage.clear()  # Clear the database to start fresh

    def tearDown(self):
        """Clears after each test"""
        with self.create_app().app_context():
            storage.clear()

    def test_signup_valid_user(self):
        """Test signing up a valid user"""
        response = self.client.post(
            "/signup",
            data=dict(
                username="newuser",
                address="123 Test St",
                email="newuser@example.com",
                password="ValidP@ssw0rd",
            ),
            follow_redirects=True,
        )

        self.assertIn(b"Account created successfully", response.data)
        self.assertEqual(response.status_code, 200)

        # Check if the user exists in the database
        with self.create_app().app_context():
            client = storage.all(Client)
            self.assertEqual(len(client), 1)
            created_user = list(client.values())[0]
            self.assertEqual(created_user.username, "newuser")
            self.assertTrue(check_password_hash(created_user.password, "ValidP@ssw0rd"))

    def test_signup_user_exists(self):
        """Test if the form prevents signing up with an existing username or email"""
        # Create a client before attempting to sign up
        with self.create_app().app_context():
            client = Client(
                username="existinguser",
                address="123 Test St",
                email="existinguser@example.com",
                password="ValidP@ssw0rd",
            )
            storage.new(client)
            storage.save()

        response = self.client.post(
            "/signup",
            data=dict(
                username="existinguser",  # Existing username
                address="123 Test St",
                email="newuser@example.com",
                password="ValidP@ssw0rd",
            ),
            follow_redirects=True,
        )
        self.assertIn(b"Username already exists! Please choose a different one", response.data)

        response = self.client.post(
            "/signup",
            data=dict(
                username="newuser",
                address="123 Test St",
                email="existinguser@example.com",  # Existing email
                password="ValidP@ssw0rd",
            ),
            follow_redirects=True,
        )
        self.assertIn(b"Email already exists! Please choose a different one", response.data)

    def test_signup_invalid_password(self):
        """Test if invalid password format is handled"""
        response = self.client.post(
            "/signup",
            data=dict(
                username="newuser",
                address="123 Test St",
                email="newuser@example.com",
                password="invalidpassword",  # Invalid password (does not meet the regex)
            ),
            follow_redirects=True,
        )
        self.assertIn(b"Invalid password format", response.data)

    def test_signup_redirect_authenticated_user(self):
        """Test if authenticated users are redirected to the welcome page"""
        with self.client:
            self.login()  # Assuming you have a login helper
            response = self.client.get("/signup", follow_redirects=True)
            self.assertRedirects(response, "/welcome")  # Adjust based on your route

    def login(self):
        """Helper method to log in a test user"""
        response = self.client.post(
            "/login",
            data=dict(email="existinguser@example.com", password="ValidP@ssw0rd"),
        )
        return response

if __name__ == "__main__":
    unittest.main()
