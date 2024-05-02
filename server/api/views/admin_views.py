"""
This module provides views for the Adminstrator in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from server.api.utils import make_response_
from server.controllers.admin_controller import AdminController
from server.exception import UnauthorizedError

admin_views = Blueprint("admin_views", __name__)

admin_controller = AdminController()


@admin_views.route("/admins/users", methods=["GET"])
@jwt_required()
@swag_from("docs/admin_views/get_all_users.yaml")
def get_all_users():
    """
    Endpoint to get all users.
    Only accessible by admin users.
    """
    try:
        users = admin_controller.get_all_users()
        return (
            make_response_(
                "success", "Fetched all users", [
                    user.to_dict for user in users
                    ]
            ),
            200,
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401


@admin_views.route("/admins/users/<user_id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/admin_views/delete_user.yaml")
def delete_user(user_id):
    """
    Endpoint to delete a specific user.
    Only accessible by admin users.
    """
    try:
        admin_controller.delete_user(user_id)
        return make_response_("success", "User deleted successfully"), 200
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@admin_views.route("/admins/users/<user_id>/disable", methods=["PUT"])
@jwt_required()
@swag_from("docs/admin_views/disable_user.yaml")
def disable_user(user_id):
    """
    Endpoint to disable a specific user.
    Only accessible by admin users.
    """
    try:
        admin_controller.disable_user(user_id)
        return make_response_("success", "User disabled successfully"), 200
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@admin_views.route("/admins/users/<user_id>/enable", methods=["PUT"])
@jwt_required()
@swag_from("docs/admin_views/enable_user.yaml")
def enable_user(user_id):
    """
    Endpoint to enable a specific user.
    Only accessible by admin users.
    """
    try:
        admin_controller.enable_user(user_id)
        return make_response_("success", "User enabled successfully"), 200
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@admin_views.route("/admins/users/<user_id>/role", methods=["PUT"])
@jwt_required()
@swag_from("docs/admin_views/change_user_role.yaml")
def change_user_role(user_id):
    """
    Endpoint to change the role of a specific user.
    Only accessible by admin users.
    """
    new_role = request.json.get("role")
    try:
        admin_controller.change_user_role(user_id, new_role)
        return make_response_("success", "User role changed successfully"), 200
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@admin_views.route("/admins/stats", methods=["GET"])
@jwt_required()
@swag_from("docs/admin_views/get_sys_statistics.yaml")
def get_sys_statistics():
    """
    Endpoint to get system statistics.
    Only accessible by admin users.
    """
    try:
        stats = admin_controller.get_sys_statistics()
        return make_response_(
                "success",
                "Fetched system statistics",
                stats
                ), 200
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
