"""
This module initializes and configures the Flask application.

The application is configured with CORS, session management,
and user authentication.
It also registers the user-related routes from the `user_views` blueprint.

Modules:
    Flask: The main class for all Flask applications.
    Bcrypt: Used for hashing passwords.
    CORS: A Flask extension for handling Cross Origin Resource Sharing (CORS),
    making cross-origin AJAX possible.
    LoginManager: Provides user session management for Flask.
    Session: Provides server-backed sessions for Flask.

Imports:
    server.api.views.user_views: Contains the user-related routes.
    server.config: Contains the application configuration.
    server.models: Contains the SQLAlchemy models and storage helper.


"""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_session import Session

from server.api.utils import make_response
from server.api.views.user_views import set_bcrypt
from server.config import ApplicationConfig
from server.models import storage
from server.models.user import User

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.url_map.strict_slashes = False

bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
server_session = Session(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Load a user given the user_id.

    Args:
        user_id (str): The unique identifier of the user.

    Returns:
        User: The User object if found, None otherwise.
    """
    return storage.get(User, user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """Redirects unauthorized users to a custom HTML page."""
    return make_response("error", "Unauthorized"), 401


@app.errorhandler(400)
def bad_request(e):
    return make_response("error", "Bad Request"), 400


@app.errorhandler(401)
def unauthorized(e):
    return make_response("error", "Unauthorized"), 401


@app.errorhandler(403)
def forbidden(e):
    return make_response("error", "Forbidden"), 403


@app.errorhandler(404)
def not_found(e):
    return make_response("error", "Not Found"), 404


@app.errorhandler(405)
def method_not_allowed(e):
    return make_response("error", "Method Not Allowed"), 405


@app.errorhandler(408)
def request_timeout(e):
    return make_response("error", "Request Timeout"), 408


@app.errorhandler(500)
def internal_server_error(e):
    return make_response("error", "Internal Server Error"), 500


set_bcrypt(bcrypt)


# Import Blueprints

from server.api.views.candidate_views import candidate_views
from server.api.views.job_views import job_views
from server.api.views.major_views import major_views
from server.api.views.recruiter_views import recruiter_views
from server.api.views.user_views import user_views

# Register Blueprints
app.register_blueprint(user_views, url_prefix="/api")
app.register_blueprint(candidate_views, url_prefix="/api")
app.register_blueprint(recruiter_views, url_prefix="/api")
app.register_blueprint(job_views, url_prefix="/api")
app.register_blueprint(major_views, url_prefix="/api")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
