#!/usr/bin/python3
"""Defines the Review class."""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Represents a review.

    Attributes:
        place_id (str): ID of the place being reviewed.
        user_id (str): ID of the user who submitted the review.
        text (str): The content of the review.
    """

    place_id = ""
    user_id = ""
    text = ""
