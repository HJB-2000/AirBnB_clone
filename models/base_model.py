#!/usr/bin/python3
"""
Defines the BaseModel class for the AirBnB clone project.

Attributes:
    BaseModel (class): The base class for all other models.
"""
import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    Serves as the base class for all other models.

    Methods:
        __init__(*args, **kwargs): Initializes a new instance.
        save(): Updates the 'updated_at' attribute and saves the instance.
        to_dict(): Returns a dictionary containing all keys/values
        of the instance.
        __str__(): Returns the string representation of the instance.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of BaseModel.

        Args:
            *args (tuple): Variable length argument list.
            **kwargs (dict): Arbitrary keyword arguments.

        Attributes:
            id (str): Unique identifier for the instance.
            created_at (datetime): Datetime when the instance was created.
            updated_at (datetime): Datetime when the instance was last updated.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        if len(kwargs) != 0:
            key_list = list(kwargs.keys())
            i = 0
            while i < len(key_list):
                key = key_list[i]
                value = kwargs[key]
                if key == "created_at" or key == "updated_at":
                    self.__dict__[key] = datetime.strptime(value, time_format)
                else:
                    self.__dict__[key] = value
                i += 1
        else:
            models.storage.new(self)

    def save(self):
        """
        Updates the 'updated_at' attribute with the current
        datetime and saves the instance.
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary containing all keys/values of the instance.

        Returns:
            dict: A dictionary containing all keys/values of the instance.
        """
        object_dict = self.__dict__.copy()
        object_dict['__class__'] = self.__class__.__name__
        object_dict['created_at'] = self.created_at.isoformat()
        object_dict['updated_at'] = self.updated_at.isoformat()
        return object_dict

    def __str__(self):
        """
        Returns the string representation of the instance.

        Returns:
            str: The string representation of the instance.
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)
