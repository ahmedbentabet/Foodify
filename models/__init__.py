#!/usr/bin/python3
"""This module instantiates an object of the DBStorage class"""
from models.engine.db_storage import DBStorage
from flask import g

storage = DBStorage()
storage.reload()

def close_db(e=None):
    """Cleanup function to be called after each request"""
    storage.close()

# Register cleanup function with Flask app
from app import foodify_app
foodify_app.teardown_appcontext(close_db)
