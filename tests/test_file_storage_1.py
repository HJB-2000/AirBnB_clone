#!/usr/bin/python3
import unittest
import sys
import os
import json
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage


class TestFileStorage(unittest.TestCase):
    """Tests for FileStorage class."""

    @classmethod
    def setUpClass(cls):
        """Set up for test suite"""
        cls.file_path = FileStorage._FileStorage__file_path
        try:
            os.rename(cls.file_path, 'tmp')
        except IOError:
            pass

    @classmethod
    def tearDownClass(cls):
        """Tear down after test suite"""
        try:
            os.remove(cls.file_path)
        except IOError:
            pass
        try:
            os.rename('tmp', cls.file_path)
        except IOError:
            pass

    def setUp(self):
        """Set up for individual test"""
        FileStorage._FileStorage__objects = {}

    def test_all_returns_dict(self):
        """Test that all() returns the __objects dictionary."""
        self.assertEqual(storage.all(), {})

    def test_new(self):
        """Test that new() correctly adds an object to __objects."""
        obj = BaseModel()
        storage.new(obj)
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], obj)

    def test_save(self):
        """Test that save() correctly serializes __objects to the file."""
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        with open(self.file_path, 'r') as f:
            obj_dict = json.load(f)
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, obj_dict)
        self.assertEqual(obj_dict[key]['id'], obj.id)

    def test_reload(self):
        """Test that reload() correctly deserializes objects from the file."""
        obj = BaseModel()
        storage.new(obj)
        storage.save()
        FileStorage._FileStorage__objects = {}
        storage.reload()
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].id, obj.id)

    def test_reload_no_file(self):
        """Test that reload() does nothing if the file does not exist."""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        storage.reload()
        self.assertEqual(storage.all(), {})


if __name__ == "__main__":
    unittest.main()
