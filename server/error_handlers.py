"""
Handlers for HTML errors
"""

from server.api.utils import make_response_


def register_error_handlers(app):
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
