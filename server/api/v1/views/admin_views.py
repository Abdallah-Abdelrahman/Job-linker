"""
This module provides views for the Adminstrator in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.admin_controller import AdminController
from server.decorators import handle_errors

# admin_views = Blueprint("admin_views", __name__)

admin_controller = AdminController()


@app_views.route("/admins/users", methods=["GET"])
@jwt_required()
@swag_from("docs/app_views/get_all_users.yaml")
@handle_errors
def get_all_users():
    """
    Endpoint to get all users.
    Only accessible by admin users.
    """
    curr_user_id = get_jwt_identity()
    users = admin_controller.get_all_users(curr_user_id)
    return (
        make_response_(
            "success", "Fetched all users", [user.to_dict for user in users]
        ),
        200,
    )


@app_views.route("/admins/users/<target_user_id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/app_views/delete_user.yaml")
@handle_errors
def delete_user(target_user_id):
    """
    Endpoint to delete a specific user.
    Only accessible by admin users.
    """
    curr_user_id = get_jwt_identity()
    admin_controller.delete_user(target_user_id, curr_user_id)
    return make_response_("success", "User deleted successfully"), 200


@app_views.route("/admins/users/<target_user_id>/disable", methods=["PUT"])
@jwt_required()
@swag_from("docs/app_views/disable_user.yaml")
@handle_errors
def disable_user(target_user_id):
    """
    Endpoint to disable a specific user.
    Only accessible by admin users.
    """
    curr_user_id = get_jwt_identity()
    admin_controller.disable_user(target_user_id, curr_user_id)
    return make_response_("success", "User disabled successfully"), 200


@app_views.route("/admins/users/<target_user_id>/enable", methods=["PUT"])
@jwt_required()
@swag_from("docs/app_views/enable_user.yaml")
@handle_errors
def enable_user(target_user_id):
    """
    Endpoint to enable a specific user.
    Only accessible by admin users.
    """
    curr_user_id = get_jwt_identity()
    admin_controller.enable_user(target_user_id, curr_user_id)
    return make_response_("success", "User enabled successfully"), 200


@app_views.route("/admins/users/<target_user_id>/role", methods=["PUT"])
@jwt_required()
@swag_from("docs/app_views/change_user_role.yaml")
@handle_errors
def change_user_role(target_user_id):
    """
    Endpoint to change the role of a specific user.
    Only accessible by admin users.
    """
    curr_user_id = get_jwt_identity()
    new_role = request.json.get("role")
    admin_controller.change_user_role(target_user_id, new_role, curr_user_id)
    return make_response_("success", "User role changed successfully"), 200


@app_views.route("/admins/stats", methods=["GET"])
@jwt_required()
@swag_from("docs/app_views/get_sys_statistics.yaml")
@handle_errors
def get_sys_statistics():
    """
    Endpoint to get system statistics.
    Only accessible by admin users.
    """
    curr_user_id = get_jwt_identity()
    stats = admin_controller.get_sys_statistics(curr_user_id)
    return make_response_("success", "Fetched system statistics", stats), 200
