import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid
from models.base_model import BaseModel

class TestBaseModel(unittest.TestCase):
    """Test class for the BaseModel class"""

    def test_initialization_with_no_arguments(self):
        """Test initialization when no arguments are passed"""
        model = BaseModel()
        self.assertTrue(isinstance(model, BaseModel))
        self.assertIsNotNone(model.id)  # Check if id is generated
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)
        self.assertEqual(model.created_at, model.updated_at)

    def test_initialization_with_arguments(self):
        """Test initialization when arguments are passed"""
        args = {
            "id": "123",
            "created_at": datetime(2022, 1, 1, 12, 0),
            "updated_at": datetime(2022, 1, 2, 12, 0),
        }
        model = BaseModel(**args)
        self.assertEqual(model.id, "123")
        self.assertEqual(model.created_at, datetime(2022, 1, 1, 12, 0))
        self.assertEqual(model.updated_at, datetime(2022, 1, 2, 12, 0))

    @patch('models.storage.new')
    @patch('models.storage.save')
    def test_save(self, mock_save, mock_new):
        """Test the save method"""
        model = BaseModel()
        old_updated_at = model.updated_at
        model.save()  # Call save method to update updated_at
        self.assertNotEqual(model.updated_at, old_updated_at)
        mock_new.assert_called_once_with(model)
        mock_save.assert_called_once()

    def test_to_dict(self):
        """Test the to_dict method"""
        model = BaseModel()
        dict_representation = model.to_dict()
        self.assertIn('__class__', dict_representation)
        self.assertEqual(dict_representation['__class__'], 'BaseModel')
        self.assertIn('created_at', dict_representation)
        self.assertIn('updated_at', dict_representation)
        self.assertIsInstance(dict_representation['created_at'], str)
        self.assertIsInstance(dict_representation['updated_at'], str)

    @patch('models.storage.delete')
    def test_delete(self, mock_delete):
        """Test the delete method"""
        model = BaseModel()
        model.delete()
        mock_delete.assert_called_once_with(model)

if __name__ == "__main__":
    unittest.main()
