import unittest
from app import create_app
from flask_login import current_user
from models import storage
from models.client import Client
from werkzeug.security import generate_password_hash

class TestLogin(unittest.TestCase):
    """Test cases for the login route"""

    @classmethod
    def setUpClass(cls):
        """Set up a test client and prepare the test database"""
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Create a test user
        cls.test_user = Client(
            email="test@example.com",
            password=generate_password_hash("password123")
        )
        with storage.session_scope() as session:
            session.add(cls.test_user)
            session.commit()

    def setUp(self):
        """Set up before every test"""
        self.client.get("/logout")  # Ensure the user is logged out before each test

    def test_login_page(self):
        """Test if the login page loads successfully"""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Log In", response.data)

    def test_login_success(self):
        """Test successful login"""
        data = {"email": "test@example.com", "password": "password123", "remember": False}
        response = self.client.post("/login", data=data, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)  # Check if the user is redirected to the welcome page
        with self.client.session_transaction() as sess:
            self.assertEqual(sess['_user_id'], str(self.test_user.id))  # Check if user is logged in

    def test_login_failure_invalid_credentials(self):
        """Test failed login due to invalid credentials"""
        data = {"email": "test@example.com", "password": "wrongpassword", "remember": False}
        response = self.client.post("/login", data=data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login Unsuccessful", response.data)  # Check error message for incorrect credentials

    def test_redirect_if_authenticated(self):
        """Test if an authenticated user is redirected away from the login page"""
        self.client.post("/login", data={"email": "test@example.com", "password": "password123"})
        response = self.client.get("/login", follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Welcome", response.data)  # Check if redirected to the welcome page

    @classmethod
    def tearDownClass(cls):
        """Tear down test resources"""
        with storage.session_scope() as session:
            session.delete(cls.test_user)
            session.commit()

if __name__ == "__main__":
    unittest.main()
