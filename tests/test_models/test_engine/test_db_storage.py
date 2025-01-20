import unittest
from unittest.mock import patch, MagicMock
from models.db_storage import DBStorage
from models.base_model import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.client import Client
from models.restaurant import Restaurant

class TestDBStorage(unittest.TestCase):
    """Test class for DBStorage"""

    def setUp(self):
        """Setup a temporary in-memory database for testing"""
        self.db_storage = DBStorage()
        self.db_storage._DBStorage__engine = create_engine('sqlite:///:memory:')
        self.db_storage.reload()  # Reload database and create tables

    def tearDown(self):
        """Close session after each test"""
        self.db_storage.close()

    @patch.object(DBStorage, 'save', return_value=None)
    def test_new(self, mock_save):
        """Test new method"""
        client = Client(email="test@foodify.com", password="password123", username="testuser", address="123 Main St")
        self.db_storage.new(client)
        mock_save.assert_called_once()

    @patch.object(DBStorage, 'get', return_value=None)
    def test_get(self, mock_get):
        """Test get method"""
        mock_get.return_value = Client(id="123")
        result = self.db_storage.get(Client, "123")
        self.assertIsInstance(result, Client)

    @patch.object(DBStorage, 'all', return_value=[])
    def test_all(self, mock_all):
        """Test all method"""
        mock_all.return_value = [Client(id="123")]
        result = self.db_storage.all(Client)
        self.assertIsInstance(result, dict)
        self.assertIn("Client.123", result)

    @patch.object(DBStorage, 'delete', return_value=None)
    def test_delete(self, mock_delete):
        """Test delete method"""
        client = Client(id="123", email="test@foodify.com")
        self.db_storage.delete(client)
        mock_delete.assert_called_once_with(client)

    @patch.object(DBStorage, 'search', return_value=[])
    def test_search(self, mock_search):
        """Test search method"""
        mock_search.return_value = [Restaurant(name="Test Restaurant", city="City")]
        filters = {"city": "City"}
        result = self.db_storage.search(Restaurant, filters)
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "Test Restaurant")

    @patch.object(DBStorage, 'count', return_value=5)
    def test_count(self, mock_count):
        """Test count method"""
        mock_count.return_value = 5
        result = self.db_storage.count(Client)
        self.assertEqual(result, 5)

    @patch.object(DBStorage, 'rollback', return_value=None)
    def test_rollback(self, mock_rollback):
        """Test rollback method"""
        self.db_storage.rollback()
        mock_rollback.assert_called_once()

    @patch.object(DBStorage, 'session_scope', return_value=None)
    def test_session_scope(self, mock_session_scope):
        """Test session_scope method"""
        with self.db_storage.session_scope() as session:
            self.assertIsNotNone(session)

if __name__ == "__main__":
    unittest.main()
