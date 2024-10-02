"""
Handlers for JWT errors
"""

from server.api.utils import make_response_


def register_jwt_handlers(jwt):
    """
    Registers JWT error handlers for the Flask application.

    Each JWT error handler returns a response with an error message and the
    appropriate HTTP status code.
    """

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            make_response_(
                "error",
                "Your token has expired. Please log in again."
                ),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return (
            make_response_(
                "error",
                "The token is invalid: {}".format(error_string)
                ),
            422,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return make_response_(
                "error",
                "Missing token: {}".format(error_string)
                ), 401

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return make_response_("error", "The token has been revoked."), 401

    @jwt.needs_fresh_token_loader
    def needs_fresh_token_callback(jwt_header, jwt_payload):
        return make_response_("error", "A fresh token is required."), 401
