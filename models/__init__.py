#!/usr/bin/python3
"""
A script to reload objects from a JSON file using FileStorage.
This script initializes a FileStorage object and
reloads objects from a JSON file.
"""
from models.engine.file_storage import FileStorage
# Create a FileStorage object
storage = FileStorage()
# Reload objects from the JSON file
storage.reload()
