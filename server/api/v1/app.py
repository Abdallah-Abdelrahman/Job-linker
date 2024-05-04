"""
This module sets up the Flask application for the Job-linker application.
"""

from server.error_handlers import register_error_handlers
from server.extensions import app, jwt
from server.jwt_handlers import register_jwt_handlers


def create_app():
    """
    Initializes the Flask application.

    Sets up error handlers, JWT handlers, and blueprints.
    """
    register_error_handlers(app)
    register_jwt_handlers(jwt)

    from server.api.v1.views import app_views

    app.register_blueprint(app_views)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)
