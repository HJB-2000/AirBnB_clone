#!/usr/bin/python3
"""Specifies unit tests for the BaseModel class in models/base_model.py.

Unit Test Classes:

TestBaseModel_Initialization
TestBaseModel_Save_Method
TestBaseModel_To_Dict_Method
"""
import os
import sys
import models
import unittest
from datetime import datetime
from time import sleep
from models.base_model import BaseModel


class TestBaseModel_Initialization(unittest.TestCase):
    """
        Unittests:
        testing the instance_creation of the BaseModel class.
    """

    def test_instance_creation_no_args(self):
        self.assertEqual(BaseModel, type(BaseModel()))

    def test_instance_stored_in_storage(self):
        self.assertIn(BaseModel(), models.storage.all().values())

    def test_id_is_string(self):
        self.assertEqual(str, type(BaseModel().id))

    def test_created_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().created_at))

    def test_updated_at_is_datetime(self):
        self.assertEqual(datetime, type(BaseModel().updated_at))

    def test_unique_ids_for_instances(self):
        model1 = BaseModel()
        model2 = BaseModel()
        self.assertNotEqual(model1.id, model2.id)

    def test_different_creation_times(self):
        model1 = BaseModel()
        sleep(0.05)
        model2 = BaseModel()
        self.assertLess(model1.created_at, model2.created_at)

    def test_different_update_times(self):
        model1 = BaseModel()
        sleep(0.05)
        model2 = BaseModel()
        self.assertLess(model1.updated_at, model2.updated_at)

    def test_string_representation(self):
        date_time = datetime.today()
        date_time_representation = repr(date_time)
        model = BaseModel()
        model.id = "4684658894651dq54168"
        model.created_at = model.updated_at = date_time
        model_str = model.__str__()
        self.assertIn("[BaseModel] (4684658894651dq54168)", model_str)
        self.assertIn("'id': '4684658894651dq54168'", model_str)
        self.assertIn("'created_at': " + date_time_representation, model_str)
        self.assertIn("'updated_at': " + date_time_representation, model_str)

    def test_unused_args(self):
        model = BaseModel(None)
        self.assertNotIn(None, model.__dict__.values())

    def test_instance_creation_with_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        model = BaseModel(id="4684658894651dq54168", created_at=date_time_iso,
                          updated_at=date_time_iso)
        self.assertEqual(model.id, "4684658894651dq54168")
        self.assertEqual(model.created_at, date_time)
        self.assertEqual(model.updated_at, date_time)

    def test_instance_creation_with_invalid_kwargs(self):
        with self.assertRaises(TypeError):
            BaseModel(id=None, created_at=None, updated_at=None)

    def test_instance_creation_with_args_and_kwargs(self):
        date_time = datetime.today()
        date_time_iso = date_time.isoformat()
        model = BaseModel("984651651", id="4684658894651dq54168",
                          created_at=date_time_iso, updated_at=date_time_iso)
        self.assertEqual(model.id, "4684658894651dq54168")
        self.assertEqual(model.created_at, date_time)
        self.assertEqual(model.updated_at, date_time)


class TestBaseModel_Save_Method(unittest.TestCase):
    """
        Unittests:
        testing the save method of the BaseModel class.
    """

    @classmethod
    def setUpClass(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDownClass(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_save_updates_updated_at(self):
        model = BaseModel()
        sleep(0.05)
        first_updated_at = model.updated_at
        model.save()
        self.assertLess(first_updated_at, model.updated_at)

    def test_multiple_saves(self):
        model = BaseModel()
        sleep(0.05)
        first_updated_at = model.updated_at
        model.save()
        second_updated_at = model.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        model.save()
        self.assertLess(second_updated_at, model.updated_at)

    def test_save_with_invalid_arg(self):
        model = BaseModel()
        with self.assertRaises(TypeError):
            model.save(None)

    def test_save_updates_file(self):
        model = BaseModel()
        model.save()
        model_id = "BaseModel." + model.id
        with open("file.json", "r") as f:
            self.assertIn(model_id, f.read())


class TestBaseModel_To_Dict_Method(unittest.TestCase):
    """
        Unittests:
        testing the to_dict method of the BaseModel class.
    """

    def test_to_dict_returns_dict(self):
        model = BaseModel()
        self.assertTrue(dict, type(model.to_dict()))

    def test_to_dict_contains_correct_keys(self):
        model = BaseModel()
        self.assertIn("id", model.to_dict())
        self.assertIn("created_at", model.to_dict())
        self.assertIn("updated_at", model.to_dict())
        self.assertIn("__class__", model.to_dict())

    def test_to_dict_contains_added_attributes(self):
        model = BaseModel()
        model.name = "alx_school"
        model.my_number = 76
        self.assertIn("name", model.to_dict())
        self.assertIn("my_number", model.to_dict())

    def test_to_dict_datetime_attributes_are_strings(self):
        model = BaseModel()
        model_dict = model.to_dict()
        self.assertEqual(str, type(model_dict["created_at"]))
        self.assertEqual(str, type(model_dict["updated_at"]))

    def test_to_dict_output(self):
        date_time = datetime.today()
        model = BaseModel()
        model.id = "4684658894651dq54168"
        model.created_at = model.updated_at = date_time
        expected_dict = {
            'id': '4684658894651dq54168',
            '__class__': 'BaseModel',
            'created_at': date_time.isoformat(),
            'updated_at': date_time.isoformat()
        }
        self.assertDictEqual(model.to_dict(), expected_dict)

    def test_to_dict_differs_from_dunder_dict(self):
        model = BaseModel()
        self.assertNotEqual(model.to_dict(), model.__dict__)

    def test_to_dict_with_invalid_arg(self):
        model = BaseModel()
        with self.assertRaises(TypeError):
            model.to_dict(None)


if __name__ == "__main__":
    unittest.main()
