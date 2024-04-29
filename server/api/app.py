"""
This module sets up the Flask application for the Job-linker application.
"""

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS

# from flask_login import LoginManager
# from flask_session import Session
from flask_jwt_extended import JWTManager

from server.api.utils import make_response_
from server.api.views.user_views import set_bcrypt
from server.config import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.url_map.strict_slashes = False

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

jwt = JWTManager(app)

# server_session = Session(app)

# login_manager = LoginManager()
# login_manager.init_app(app)


# @login_manager.user_loader
# def load_user(user_id):
#    """
#    Load a user given the user_id.
#
#    Args:
#        user_id (str): The unique identifier of the user.
#
#    Returns:
#        User: The User object if found, None otherwise.
#    """
#    return storage.get(User, user_id)


# @login_manager.unauthorized_handler
# def unauthorized():
#    """Redirects unauthorized users to a custom HTML page."""
#    return make_response_("error", "Unauthorized"), 401


@app.errorhandler(400)
def bad_request(e):
    """
    Handles 400 Bad Request errors.
    """
    return make_response_("error", "Bad Request"), 400


@app.errorhandler(401)
def unauthorized(e):
    """
    Handles 401 Unauthorized errors.
    """
    return make_response_("error", "Unauthorized"), 401


@app.errorhandler(403)
def forbidden(e):
    """
    Handles 403 Forbidden errors.
    """
    return make_response_("error", "Forbidden"), 403


@app.errorhandler(404)
def not_found(e):
    """
    Handles 404 Not Found errors.
    """
    return make_response_("error", "Not Found"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    """
    Handles 405 Method Not Allowed errors.
    """
    return make_response_("error", "Method Not Allowed"), 405


@app.errorhandler(408)
def request_timeout(e):
    """
    Handles 408 Request Timeout errors.
    """
    return make_response_("error", "Request Timeout"), 408


@app.errorhandler(413)
def file_exceed(e):
    """
    Handles 413 error when file exceeds 2mb.
    """
    return make_response_("error", "File is greater than 2MB"), 413


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handles 500 Internal Server Error errors.
    """
    return make_response_("error", "Internal Server Error"), 500


set_bcrypt(bcrypt)


# Import Blueprints

from server.api.views.application_views import application_views
from server.api.views.candidate_views import candidate_views
from server.api.views.job_views import job_views
from server.api.views.language_views import language_views
from server.api.views.major_views import major_views
from server.api.views.recruiter_views import recruiter_views
from server.api.views.skill_views import skill_views
from server.api.views.user_views import user_views
from server.api.views.work_experience_views import work_experience_views
from server.api.views.file_views import file_views

# Register Blueprints

app.register_blueprint(user_views, url_prefix="/api")
app.register_blueprint(candidate_views, url_prefix="/api")
app.register_blueprint(recruiter_views, url_prefix="/api")
app.register_blueprint(job_views, url_prefix="/api")
app.register_blueprint(major_views, url_prefix="/api")
app.register_blueprint(skill_views, url_prefix="/api")
app.register_blueprint(work_experience_views, url_prefix="/api")
app.register_blueprint(language_views, url_prefix="/api")
app.register_blueprint(application_views, url_prefix="/api")
app.register_blueprint(file_views, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
