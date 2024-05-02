"""
This module provides views for the User model in the Job-linker application.
"""
from flasgger.utils import swag_from
from flask import  request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_refresh_cookies,
)

from server.api.utils import make_response_
from server.decorators import verified_required
from server.exception import UnauthorizedError
from server.api.v1.views import app_views


bcrypt = None
user_controller = None


def setup(controller):
    """
    Sets the bcrypt instance for password hashing.

    Args:
        bcrypt_instance: The bcrypt instance.
    """
    global user_controller
    user_controller = controller


@app_views.route("/register", methods=["POST"])
@swag_from("docs/app_views/register_user.yaml")
def register_user():
    """
    Registers a new user.

    Returns:
        A response object containing the status, message, and user data
        if successful.
        Otherwise, it returns an error message.
    """
    try:
        new_user = user_controller.register_user(request.json)
        response = make_response_(
            "success",
            "User registered successfully",
            {"role": new_user.role},
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400

    return response, 201


@app_views.route("/verify", methods=["GET"])
@swag_from("docs/app_views/verify_email.yaml")
def verify_email():
    """
    Verifies a user's email.

    Args:
        token (str): The verification token.

    Returns:
        A response object containing the status and message.
    """
    verf_token = request.query_string.decode("utf8").split("=")[-1]
    try:
        jwt, jwt_refresh, user = user_controller.verify_email(verf_token)

        resp = make_response_(
            "success",
            "User logged in successfully",
            {"role": user.role, "name": user.name, "jwt": jwt},
        )

        set_refresh_cookies(resp, jwt_refresh)
        return resp, 200
    except ValueError as e:
        return make_response_("error", str(e)), 400


@app_views.route("/login", methods=["POST"])
@swag_from("docs/app_views/login_user.yaml")
def login_user():
    """
    Logs in a user.

    Returns:
        A response object containing the status, message, and user data
        if successful.
        Otherwise, it returns an error message.
    """
    try:
        user, access_token, refresh_token = user_controller.login_user(
                request.json
                )
        response_data = make_response_(
            "success",
            "User logged in successfully",
            {"role": user.role, "jwt": access_token},
        )
    except ValueError as e:
        return make_response_("error", str(e)), 401
    except UnauthorizedError as e:
        return make_response_("error", str(e)), 200

    response = response_data
    set_refresh_cookies(response, refresh_token)
    return response


@app_views.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations="cookies")
@swag_from("docs/app_views/refresh_token.yaml")
def refresh_token():
    """
    Route to refresh the JWT token for a user.

    This route requires a valid refresh token in the cookies. It creates a new
    access token for the user and returns it in the response. The user ID is
    extracted from the current identity in the JWT.

    Returns:
        Response: A response object with a success message and the new JWT.
    """
    user_id = get_jwt_identity()
    jwt = create_access_token(identity=user_id)
    return (
        make_response_(
            "success",
            "Token refreshed successfully",
            {"jwt": jwt},
        ),
        200,
    )


@app_views.route("/logout", methods=["POST"])
@jwt_required()
@verified_required
@swag_from("docs/app_views/logout_user.yaml")
def logout_user():
    """
    Logs out a user.

    Returns:
        A response object containing the status and message.
    """
    return make_response_("success", "Logged out successfully")


@app_views.route("/@me")
@jwt_required()
@verified_required
@swag_from("docs/app_views/get_current_user.yaml")
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
        user_data = user_controller.get_current_user(user_id)
        return make_response_(
            "success",
            "User details fetched successfully",
            user_data,
        )
    except ValueError as e:
        return make_response_("error", str(e)), 401


@app_views.route("/@me", methods=["PUT"])
@jwt_required()
@verified_required
@swag_from("docs/app_views/update_current_user.yaml")
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


@app_views.route("/@me", methods=["DELETE"])
@jwt_required()
@verified_required
#@swag_from("docs/app_views/delete_current_user.yaml")
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


@app_views.route("/@me/password", methods=["PUT"])
@jwt_required()
@verified_required
@swag_from("docs/app_views/update_password.yaml")
def update_password():
    """
    Updates the current user's password.

    Returns:
        A response object containing the status and message.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    current_password = request.json.get("current_password")
    new_password = request.json.get("new_password")

    try:
        user_controller.update_password(
                user_id,
                current_password,
                new_password
                )
        return make_response_("success", "Password updated successfully")
    except ValueError as e:
        return make_response_("error", str(e)), 400
