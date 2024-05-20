#!/usr/bin/python3
import json
from collections import OrderedDict
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class FileStorage:
    """
    A class to manage storage of objects in a JSON file.

    Attributes:
    __file_path (str): The file path for storing JSON data.
    __objects (dict): A dictionary to store objects.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Retrieves all objects stored in the file.

        Returns:
        dict: A dictionary containing all stored objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the storage.

        Args:
        obj: The object to be added to storage.
        """
        object_name = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(object_name, obj.id)] = obj

    def save(self):
        """
        Saves objects to the JSON file.
        """
        objects = FileStorage.__objects
        object_dict = OrderedDict(
            ("{}.{}".format(obj.__class__.__name__, obj.id), obj.to_dict())
            for obj in objects.values()
        )
        with open(FileStorage.__file_path, "w") as file:
            json.dump(object_dict, file)

    def reload(self):
        """
        Reloads objects from the JSON file.
        """
        try:
            with open(FileStorage.__file_path) as file:
                object_dict = json.load(file, object_pairs_hook=OrderedDict)
                for object_id, object_data in object_dict.items():
                    class_name = object_data["__class__"]
                    del object_data["__class__"]
                    self.new(eval(class_name)(**object_data))
        except FileNotFoundError:
            return

storage = FileStorage()
