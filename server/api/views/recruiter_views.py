"""
This module provides views for the Recruiter model in the
Job-linker application.
"""

from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.controllers.recruiter_controller import RecruiterController

recruiter_views = Blueprint("recruiter", __name__)

recruiter_controller = RecruiterController()


@recruiter_views.route("/recruiters", methods=["POST"])
@jwt_required()
def create_recruiter():
    """
    Creates a new recruiter.

    Returns:
        A response object containing the status, message, and recruiter
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        new_recruiter = recruiter_controller.create_recruiter(
                user_id,
                request.json
                )
        return (
            make_response_(
                "success",
                "Recruiter created successfully",
                {"id": new_recruiter.id},
            ),
            201,
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400


@recruiter_views.route("/recruiters/@me", methods=["GET"])
@jwt_required()
def get_current_recruiter():
    """
    Fetches the current recruiter's details.

    Returns:
        A response object containing the status, message, and recruiter
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        recruiter = recruiter_controller.get_current_recruiter(user_id)
        return make_response_(
            "success",
            "Recruiter details fetched successfully",
            {
                "id": recruiter.id,
                "company_name": recruiter.company_name,
                "company_info": recruiter.company_info,
            },
        )
    except ValueError as e:
        return make_response_("error", str(e)), 404


@recruiter_views.route("/recruiters/@me", methods=["PUT"])
@jwt_required()
def update_current_recruiter():
    """
    Updates the current recruiter's details.

    Returns:
        A response object containing the status, message, and recruiter
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        recruiter = recruiter_controller.update_current_recruiter(
                user_id,
                request.json
                )
        return make_response_(
            "success",
            "Recruiter details updated successfully",
            {
                "id": recruiter.id,
                "company_name": recruiter.company_name,
                "company_info": recruiter.company_info,
            },
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400
