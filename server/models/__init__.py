#!/usr/bin/env python3
'''Module creates a unique DBStorage instance for the application

Attrs:
    storage: an instance of DBStorage
'''

from models.engine.db import DBStorage
from os import getenv


storage = DBStorage()
storage.reload()
