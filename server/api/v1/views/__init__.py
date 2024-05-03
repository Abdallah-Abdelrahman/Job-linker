#!/usr/bin/python3
""" Blueprint for API

Attrs:
    app_views: app blue print
    user_controller: instance of user controller with added encryption
"""
from flask import Blueprint
from server.controllers.user_controller import UserController


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
user_controller = UserController.with_encrypt()

if app_views:
    from server.api.v1.views.admin_views import *
    from server.api.v1.views.application_views import *
    from server.api.v1.views.candidate_views import *
    from server.api.v1.views.file_views import *
    from server.api.v1.views.language_views import *
    from server.api.v1.views.major_views import *
    from server.api.v1.views.recruiter_views import *
    from server.api.v1.views.skill_views import *
    from server.api.v1.views.user_views import *
    from server.api.v1.views.work_experience_views import *
    from server.api.v1.views.job_views import *
