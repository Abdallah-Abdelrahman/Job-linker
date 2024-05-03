from functools import wraps

from flask_jwt_extended import get_jwt_identity

from server.api.utils import make_response_
from server.controllers.user_controller import UserController


def verified_required(fn):
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
