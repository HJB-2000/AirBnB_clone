#!/usr/bin/python3
"""Defines the Place class."""
from models.base_model import BaseModel


class Place(BaseModel):
    """
    Describes a place.

    Attributes:
        city_id (str): Identifier for the city.
        user_id (str): Identifier for the user.
        name (str): Name of this place.
        description (str): Description of this place.
        number_rooms (int): Total rooms available.
        number_bathrooms (int): Number of bathrooms available.
        max_guest (int): Maximum number of guests allowed.
        price_by_night (int): Nightly rental price.
        latitude (float): Latitude coordinate.
        longitude (float): Longitude coordinate.
        amenity_ids (list): IDs of amenities available.

    """

    city_id = ""
    user_id = ""
    name = ""
    description = ""
    number_rooms = 0
    number_bathrooms = 0
    max_guest = 0
    price_by_night = 0
    latitude = 0.0
    longitude = 0.0
    amenity_ids = []
