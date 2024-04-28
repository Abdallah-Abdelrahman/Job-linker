"""
This module provides views for the User model in the Job-linker application.
"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.controllers.user_controller import UserController

user_views = Blueprint("user", __name__)

bcrypt = None
user_controller = None


def set_bcrypt(bcrypt_instance):
    """
    Sets the bcrypt instance for password hashing.

    Args:
        bcrypt_instance: The bcrypt instance.
    """
    global bcrypt, user_controller
    bcrypt = bcrypt_instance
    user_controller = UserController(bcrypt)


@user_views.route("/register", methods=["POST"])
def register_user():
    """
    Registers a new user.

    Returns:
        A response object containing the status, message, and user data
        if successful.
        Otherwise, it returns an error message.
    """
    try:
        new_user, access_token = user_controller.register_user(request.json)
        return (
            make_response_(
                "success",
                "User registered successfully",
                {"access_token": access_token, "role": new_user.role},
            ),
            201,
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400


@user_views.route("/login", methods=["POST"])
def login_user():
    """
    Logs in a user.

    Returns:
        A response object containing the status, message, and user data
        if successful.
        Otherwise, it returns an error message.
    """
    try:
        user, access_token = user_controller.login_user(request.json)
        return make_response_(
            "success",
            "User logged in successfully",
            {"access_token": access_token, "role": user.role},
        )
    except ValueError as e:
        return make_response_("error", str(e)), 401


@user_views.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    """
    Logs out a user.

    Returns:
        A response object containing the status and message.
    """
    return make_response_("success", "Logged out successfully")


@user_views.route("/@me")
@jwt_required()
def get_current_user():
    """
    Fetches the current user's details.

    Returns:
        A response object containing the status, message, and user
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        user = user_controller.get_current_user(user_id)
        return make_response_(
            "success",
            "User details fetched successfully",
            {"id": user.id, "role": user.role},
        )
    except ValueError as e:
        return make_response_("error", str(e)), 401


@user_views.route("/@me", methods=["PUT"])
@jwt_required()
def update_current_user():
    """
    Updates the current user's details.

    Returns:
        A response object containing the status, message, and user
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        user = user_controller.update_current_user(user_id, request.json)
        return make_response_(
            "success",
            "User details updated successfully",
            {"id": user.id, "role": user.role},
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400


@user_views.route("/@me", methods=["DELETE"])
@jwt_required()
def delete_current_user():
    """
    Deletes the current user.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        user_controller.delete_current_user(user_id)
        return make_response_("success", "User deleted successfully")
    except ValueError as e:
        return make_response_("error", str(e)), 401
