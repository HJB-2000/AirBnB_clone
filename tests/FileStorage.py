#!/usr/bin/python3
import unittest
from unittest.mock import patch, mock_open
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models import storage
import os  # Add this import statement


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = storage
        self.file_path = self.storage._FileStorage__file_path
        self.storage._FileStorage__objects = {}
        self.base_model = BaseModel()
        self.user = User()
        self.state = State()
        self.city = City()
        self.place = Place()
        self.amenity = Amenity()
        self.review = Review()

    # Add other test methods here

    def test_attributes(self):
        self.assertEqual(self.file_path, "file.json")
        self.assertIsInstance(self.storage._FileStorage__objects, dict)

    def test_new_method(self):
        self.storage.new(self.state)
        key = "State.{}".format(self.state.id)
        self.assertIn(key, self.storage._FileStorage__objects)

    def test_reload_method(self):
        obj_dict = {
            "BaseModel.1234": {"__class__": "BaseModel", "id":
                               "1234", "name": "Test"},
            # Add other objects as needed
        }
        # Mock the load method to return obj_dict
        with patch('json.load', return_value=obj_dict):
            self.storage.reload()
        key = "BaseModel.1234"
        self.assertIn(key, self.storage._FileStorage__objects)

    def tearDown(self):
        if os.path.exists(self.file_path):  # Fix 'path' to 'os.path'
            os.remove(self.file_path)


if __name__ == '__main__':
    unittest.main()
