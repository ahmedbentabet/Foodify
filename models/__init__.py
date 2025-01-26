#!/usr/bin/python3
"""
Database storage initialization module.
Instantiates the storage engine and makes it available throughout
the application.
"""
from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()
