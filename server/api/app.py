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

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.url_map.strict_slashes = False

CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})
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

    Sets up the bcrypt instance, user controller, registers
    error handlers, and blueprints.
    Also sets up the user views.
    """
    bcrypt = Bcrypt(app)
    user_controller = UserController(bcrypt)

    @app.before_request
    @jwt_required(optional=True)
    def before_request():
        g.user_controller = user_controller
        user_id = get_jwt_identity()
        if user_id is not None:
            g.user = storage.get(User, user_id)
        else:
            g.user = None

    register_error_handlers()
    register_blueprints()

    import server.api.views.user_views as user_views

    user_views.setup(user_controller)


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


def register_blueprints():
    """
    Registers blueprints for the Flask application.

    Each blueprint corresponds to a different part of the application,
    such as users, jobs, skills, etc.
    """
    from server.api.views.admin_views import admin_views
    from server.api.views.application_views import application_views
    from server.api.views.candidate_views import candidate_views
    from server.api.views.file_views import file_views
    from server.api.views.job_views import job_views
    from server.api.views.language_views import language_views
    from server.api.views.major_views import major_views
    from server.api.views.recruiter_views import recruiter_views
    from server.api.views.skill_views import skill_views
    from server.api.views.user_views import user_views
    from server.api.views.work_experience_views import work_experience_views

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
    app.register_blueprint(admin_views, url_prefix="/api")


if __name__ == "__main__":
    create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
