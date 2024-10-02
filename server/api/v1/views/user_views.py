"""
This module provides views for the User model in the Job-linker application.
"""
from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_refresh_cookies,
    unset_jwt_cookies,
)

from server.api.utils import make_response_
from server.api.v1.views import app_views, user_controller
from server.config import ApplicationConfig
from server.decorators import handle_errors, verified_required


@app_views.route("/register", methods=["POST"])
@handle_errors
@swag_from("docs/app_views/register_user.yaml")
def register_user():
    """
    Registers a new user.

    Returns:
        A response object containing the status, message, and user data
        if successful.
        Otherwise, it returns an error message.
    """
    new_user = user_controller.register_user(request.json)
    response = make_response_(
        "success",
        "User registered successfully",
        {"role": new_user.role},
    )
    return response, 201


@app_views.route("/verify", methods=["GET"])
@handle_errors
@swag_from("docs/app_views/verify_email.yaml")
def verify_email():
    """
    Verifies a user"s email.

    Args:
        token (str): The verification token.

    Returns:
        A response object containing the status and message.
    """
    verf_token = request.query_string.decode("utf8").split("=")[-1]
    print("------verify------>", verf_token)
    jwt, jwt_refresh, user = user_controller.verify_email(verf_token)

    resp = make_response_(
        "success",
        "User logged in successfully",
        {"role": user.role, "name": user.name, "jwt": jwt},
    )

    set_refresh_cookies(resp, jwt_refresh)
    return resp, 200


@app_views.route("/login", methods=["POST"])
@handle_errors
@swag_from("docs/app_views/login_user.yaml")
def login_user():
    """
    Logs in a user.

    Returns:
        A response object containing the status, message, and user data
        if successful.
        Otherwise, it returns an error message.
    """
    user, access_token, refresh_token = user_controller.login_user(request.json)
    response_data = make_response_(
        status="success",
        message="User logged in successfully",
        data={"role": user.role, "jwt": access_token},
        cookies={
            'refresh_token': {'value': refresh_token, 'max_age': 86400},
            'access_token': {'value': access_token, 'max_age': 3600}
        }
    )
    return response_data

@app_views.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
@handle_errors
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
    user = user_controller.get_current_user(user_id)
    jwt = create_access_token(identity=user_id)
    return make_response_(
        status="success",
        message="Token refreshed successfully",
        data={"jwt": jwt, "role": user.get("role")},
        cookies={
            'access_token': {'value': jwt, 'max_age': 3600}
        }
    )


@app_views.route("/logout", methods=["DELETE"])
@jwt_required(verify_type=False)
@verified_required
@swag_from("docs/app_views/logout_user.yaml")
def logout_user():
    """
    Endpoint for revoking the current users access token. Save the JWTs unique
    identifier (jti) in redis. Also set a Time to Live (TTL)  when storing the
    JWT so that it will automatically be cleared out of redis after the token
    expires.

    Returns:
        A response object containing the status and message.
    """
    from server.api.v1.app import jwt_redis_blocklist

    token = get_jwt()
    jti = token.get("jti")
    ttype = token.get("type")
    jwt_redis_blocklist.set(
            jti,
            "",
            ex=ApplicationConfig.JWT_ACCESS_TOKEN_EXPIRES
            )
    print(f"--------> {ttype.capitalize()} token successfully revoked")
    resp = make_response_("success", "Access token revoked successfully")
    unset_jwt_cookies(resp)
    return resp


@app_views.route("/@me")
@app_views.route("/@me/<id>")
@jwt_required()
# @cache.cached(timeout=10)
@verified_required
@handle_errors
@swag_from("docs/app_views/get_current_user.yaml")
def get_current_user(id=None):
    """
    Fetches the current user"s details.

    Returns:
        A response object containing the status, message, and user
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    user_data = user_controller.get_current_user(id or user_id)
    return make_response_(
        "success",
        "User details fetched successfully",
        user_data,
    )


@app_views.route("/@me", methods=["PUT"])
@jwt_required()
@verified_required
@handle_errors
@swag_from("docs/app_views/update_current_user.yaml")
def update_current_user():
    """
    Updates the current user"s details.

    Returns:
        A response object containing the status, message, and user
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    user = user_controller.update_current_user(user_id, request.json)
    return make_response_(
        "success",
        "User details updated successfully",
        {"id": user.id, "role": user.role},
    )


@app_views.route("/upload_profile_image", methods=["POST"])
@jwt_required()
@verified_required
@handle_errors
def upload_profile_image():
    """
    Uploads a profile image for the current user.

    Returns:
        A response object with the status, message, and data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    if "file" not in request.files:
        return make_response_("error", "No file part"), 400

    file = request.files["file"]
    if file.filename == "":
        return make_response_("error", "No selected file"), 400

    message, data, status_code = user_controller.upload_profile_image(
            user_id,
            file
            )
    return make_response_("success", message, data), status_code


@app_views.route("/@me", methods=["DELETE"])
@jwt_required()
@verified_required
@handle_errors
@swag_from("docs/app_views/delete_current_user.yaml")
def delete_current_user():
    """
    Deletes the current user.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    user_controller.delete_current_user(user_id)
    return make_response_("success", "User deleted successfully")


@app_views.route("/@me/password", methods=["PUT"])
@jwt_required()
@verified_required
@handle_errors
@swag_from("docs/app_views/update_password.yaml")
def update_password():
    """
    Updates the current user"s password.

    Returns:
        A response object containing the status and message.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    current_password = request.json.get("current_password")
    new_password = request.json.get("new_password")

    user_controller.update_password(user_id, current_password, new_password)
    return make_response_("success", "Password updated successfully")
