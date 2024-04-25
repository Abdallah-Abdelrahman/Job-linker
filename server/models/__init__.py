#!/usr/bin/env python3
'''Module creates a unique DBStorage instance for the application

Attrs:
    storage: an instance of DBStorage
'''

from server.models.engine.db import DBStorage

storage = DBStorage(engine='sqlite:///ats.db')
storage.reload()
