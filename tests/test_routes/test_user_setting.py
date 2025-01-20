import unittest
from flask import Flask
from flask_testing import TestCase
from flask_login import current_user
from app import create_app
from models import storage
from models.client import Client
from werkzeug.security import check_password_hash


class TestUserSettingsRoute(TestCase):
    def create_app(self):
        app = create_app("testing")  # Use testing configuration
        return app

    def setUp(self):
        """Sets up the test environment before each test"""
        with self.create_app().app_context():
            storage.clear()  # Clear the database before each test
            # Create a test client in the database
            client = Client(
                username="testuser",
                address="123 Test St",
                email="testuser@example.com",
                password="TestP@ssw0rd",
            )
            storage.new(client)
            storage.save()

    def tearDown(self):
        """Clears after each test"""
        with self.create_app().app_context():
            storage.clear()

    def test_update_user_settings(self):
        """Test updating user settings successfully"""
        # Login as the test client
        self.login()

        # Update the user settings
        response = self.client.post(
            "/setting",
            data=dict(
                username="updateduser",
                address="456 New St",
                email="updateduser@example.com",
                current_password="TestP@ssw0rd",
                new_password="NewP@ssw0rd123",
            ),
            follow_redirects=True,
        )

        # Check if the settings have been updated
        self.assertIn(b"Profile information updated successfully!", response.data)
        self.assertIn(b"Password updated successfully!", response.data)

        # Check if the changes were saved in the database
        with self.create_app().app_context():
            client = storage.all(Client).values()
            updated_user = list(client)[0]
            self.assertEqual(updated_user.username, "updateduser")
            self.assertEqual(updated_user.address, "456 New St")
            self.assertEqual(updated_user.email, "updateduser@example.com")
            self.assertTrue(
                check_password_hash(updated_user.password, "NewP@ssw0rd123")
            )

    def test_update_email_exists(self):
        """Test if the form prevents updating to an existing email"""
        # Create another test client
        with self.create_app().app_context():
            client2 = Client(
                username="anotheruser",
                address="789 Another St",
                email="anotheruser@example.com",
                password="AnotherP@ssw0rd",
            )
            storage.new(client2)
            storage.save()

        # Login as the first test client
        self.login()

        # Attempt to update to an existing email
        response = self.client.post(
            "/setting",
            data=dict(
                username="updateduser",
                address="456 New St",
                email="anotheruser@example.com",  # Existing email
                current_password="TestP@ssw0rd",
                new_password="NewP@ssw0rd123",
            ),
            follow_redirects=True,
        )

        self.assertIn(b"Email already exists! Please choose a different one", response.data)

    def test_update_invalid_current_password(self):
        """Test if the current password is validated before updating the password"""
        # Login as the test client
        self.login()

        # Attempt to update password with incorrect current password
        response = self.client.post(
            "/setting",
            data=dict(
                username="testuser",
                address="123 Test St",
                email="testuser@example.com",
                current_password="WrongP@ssw0rd",  # Incorrect password
                new_password="NewP@ssw0rd123",
            ),
            follow_redirects=True,
        )

        self.assertIn(b"Current password is incorrect", response.data)

    def test_update_without_current_password(self):
        """Test if current password is required when setting a new password"""
        # Login as the test client
        self.login()

        # Attempt to update password without providing the current password
        response = self.client.post(
            "/setting",
            data=dict(
                username="testuser",
                address="123 Test St",
                email="testuser@example.com",
                current_password="",  # Empty current password
                new_password="NewP@ssw0rd123",
            ),
            follow_redirects=True,
        )

        self.assertIn(b"Current password is required to set new password", response.data)

    def login(self):
        """Helper method to log in a test user"""
        response = self.client.post(
            "/login",
            data=dict(email="testuser@example.com", password="TestP@ssw0rd"),
        )
        return response


if __name__ == "__main__":
    unittest.main()
