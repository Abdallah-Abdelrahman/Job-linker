#!/usr/bin/python3
""" Blueprint for API

Attrs:
    app_views2: app blue print
"""
from flask import Blueprint


app_views2 = Blueprint('app_views2', __name__, url_prefix='/api/v2')

if app_views2:
    from server.api.v2.views.file_views import *
