"""
This module defines the user-related routes for the Flask application.

The routes include user registration, login, logout, and fetching the
current user's details.
Each route validates the incoming data using the appropriate Marshmallow
schema and performs the necessary operations.

Modules:
    flask: The main class for all Flask applications.
    flask_login: Provides user session management for Flask.
    marshmallow: Used for data validation.
    server.models: Contains the SQLAlchemy models and storage helper.
    server.models.user: The User SQLAlchemy model.
    .schemas: Contains the data validation schemas for user login and
    registration.

Functions:
    set_bcrypt(bcrypt_instance): Sets bcrypt instance for password hashing.
    make_response(status, message, data): Creates a unified response format.
"""
from flask import Blueprint, request, session
from flask_login import login_required, login_user, logout_user
from marshmallow import ValidationError

from server.api.utils import make_response
from server.models import storage
from server.models.user import User

from .schemas import login_schema, registration_schema, update_schema

user_views = Blueprint("user", __name__)


def set_bcrypt(bcrypt_instance):
    """
    Sets the bcrypt instance for password hashing.

    Args:
        bcrypt_instance: The bcrypt instance.
    """
    global bcrypt
    bcrypt = bcrypt_instance


@user_views.route("/register", methods=["POST"])
def register_user():
    """
    Handles user registration.

    Validates the incoming data and creates a new user if the validation
    is successful.
    """
    try:
        data = registration_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user = storage.get_by_attr(User, "email", data["email"])
    if user:
        return make_response("error", "User already exists"), 409

    hashed_password = bcrypt.generate_password_hash(data["password"])
    new_user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_password,
        role=data["role"],
    )
    storage.new(new_user)
    storage.save()

    session["user_id"] = new_user.id
    session["role"] = new_user.role

    return (
        make_response(
            "success",
            "User registered successfully",
            {"id": new_user.id, "role": new_user.role},
        ),
        201,
    )


@user_views.route("/login", methods=["POST"])
def login_user_():
    """
    Handles user login.

    Validates the incoming data and logs in the user if the validation is
    successful.
    """
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user = storage.get_by_attr(User, "email", data["email"])
    if not user or not bcrypt.check_password_hash(
            user.password,
            data["password"]
            ):
        return make_response("error", "Unauthorized"), 401

    login_user(user)
    session["user_id"] = user.id
    session["role"] = user.role

    return make_response(
        "success",
        "User logged in successfully",
        {"id": user.id, "role": user.role}
    )


@user_views.route("/logout", methods=["POST"])
@login_required
def logout_user_():
    """
    Handles user logout.

    Logs out the user if they are currently logged in.
    """
    if "user_id" in session:
        session.pop("user_id")
        session.pop("role")
        logout_user()
        return make_response("success", "Logged out successfully")
    else:
        return make_response("error", "No active session"), 400


@user_views.route("/@me")
@login_required
def get_current_user():
    """
    Fetches the current user's details.

    Returns the details of the user who is currently logged in.
    """
    user_id = session.get("user_id")
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    user = storage.get(User, user_id)
    return make_response(
        "success",
        "User details fetched successfully",
        {"id": user.id, "role": user.role},
    )


@user_views.route("/@me", methods=["PUT"])
@login_required
def update_current_user():
    """Update the current user's details."""
    try:
        data = update_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user_id = session.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        return make_response("error", "Unauthorized"), 401

    for key, value in data.items():
        setattr(user, key, value)
    storage.save()

    return make_response(
        "success",
        "User details updated successfully",
        {"id": user.id, "role": user.role},
    )


@user_views.route("/@me", methods=["DELETE"])
@login_required
def delete_current_user():
    """Delete the current user."""
    user_id = session.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        return make_response("error", "Unauthorized"), 401

    storage.delete(user)
    storage.save()

    session.pop("user_id")
    session.pop("role")
    logout_user()

    return make_response("success", "User deleted successfully")
