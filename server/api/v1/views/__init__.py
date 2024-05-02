#!/usr/bin/python3
""" Blueprint for API """
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

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
