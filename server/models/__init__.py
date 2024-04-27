#!/usr/bin/env python3
"""Module creates a unique DBStorage instance for the application

Attrs:
    storage: an instance of DBStorage
"""

from os import getenv
from server.models.engine.db_storage import DBStorage

storage = DBStorage(engine=getenv('ENGINE'))
storage.reload()
