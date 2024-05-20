#!/usr/bin/python3
"""This script defines the Amenity class."""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """A class representing an amenity.
    Attributes:
        name (str): The name of the amenity.
    """

    name = ""
