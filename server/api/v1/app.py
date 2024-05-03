"""
This module sets up the Flask application for the Job-linker application.
"""

from flasgger import Swagger
from flask import Flask, g
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from server.api.utils import make_response_
from server.config import ApplicationConfig
from server.controllers.user_controller import UserController
from server.models import storage
from server.models.user import User
from server.api.v1.views import app_views

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.url_map.strict_slashes = False
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
jwt = JWTManager(app)

swagger = Swagger(app)
swagger.config["title"] = "Job Linker API"
swagger.config["version"] = "0.0.1"
swagger.config[
        "description"
        ] = "API End-points to interact with the application"


def create_app():
    """
    Initializes the Flask application.

    it sets up error handlers, and blueprints.
    """

    register_error_handlers()
    app.register_blueprint(app_views)


def register_error_handlers():
    """
    Registers error handlers for the Flask application.

    Each error handler returns a response with an error message and the
    appropriate HTTP status code.
    """

    @app.errorhandler(400)
    def bad_request(e):
        return make_response_("error", "Bad Request"), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return make_response_("error", "Unauthorized"), 401

    @app.errorhandler(403)
    def forbidden(e):
        return make_response_("error", "Forbidden"), 403

    @app.errorhandler(404)
    def not_found(e):
        return make_response_("error", "Not Found"), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return make_response_("error", "Method Not Allowed"), 405

    @app.errorhandler(408)
    def request_timeout(e):
        return make_response_("error", "Request Timeout"), 408

    @app.errorhandler(413)
    def file_exceed(e):
        return make_response_("error", "File is greater than 2MB"), 413

    @app.errorhandler(500)
    def internal_server_error(e):
        return make_response_("error", "Internal Server Error"), 500


if __name__ == "__main__":
    create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
