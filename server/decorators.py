from functools import wraps

from flask_jwt_extended import get_jwt_identity

from server.api.utils import make_response_
from server.controllers.user_controller import UserController
from server.exception import UnauthorizedError


def verified_required(fn):
    """
    Decorator to ensure the user is verified.

    This decorator retrieves the user's identity from the JWT token,
    fetches the user from the database, and checks if the user's email
    is verified. If the user is not found or their email is not verified,
    it returns an error response.

    Args:
        fn (function): The function to decorate.

    Returns:
        function: The decorated function.
    """

    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        try:
            user = UserController.with_encrypt().get_user(user_id)
        except ValueError as e:
            return make_response_("error", str(e)), 400
        if not user.verified:
            return make_response_("error", "Email not verified"), 400
        return fn(*args, **kwargs)

    return wrapper


def handle_errors(f):
    """
    Decorator to handle common errors.

    This decorator wraps a function and handles UnauthorizedError and
    ValueError exceptions.
    If one of these exceptions is raised, it returns an error response.

    Args:
        f (function): The function to decorate.

    Returns:
        function: The decorated function.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except UnauthorizedError as e:
            return make_response_("error", str(e)), 401
        except ValueError as e:
            return make_response_("error", str(e)), 400
        except Exception as e:
            return (
                make_response_(
                    "error",
                    "An unexpected error occurred: " + str(e)
                    ),
                500,
            )

    return decorated_function
