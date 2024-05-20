#!/usr/bin/python3
"""Defines the User class."""
from models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user.

    Attributes:
        email (str): Email address of the user.
        password (str): Password of the user.
        first_name (str): First name of the user.
        last_name (str): Last name of the user.
    """

    email = ""
    password = ""
    first_name = ""
    last_name = ""
