"""
This module provides views for the Recruiter model in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.recruiter_controller import RecruiterController
from server.decorators import handle_errors

recruiter_controller = RecruiterController()


@app_views.route("/recruiters", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/create_recruiter.yaml")
def create_recruiter():
    """
    Creates a new recruiter.

    Returns:
        A response object containing the status, message, and recruiter
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
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


@app_views.route("/recruiters/@me", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_current_recruiter.yaml")
def get_current_recruiter():
    """
    Fetches the current recruiter's details.

    Returns:
        A response object containing the status, message, and recruiter
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
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


@app_views.route("/recruiters/@me", methods=["PUT"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/update_current_recruiter.yaml")
def update_current_recruiter():
    """
    Updates the current recruiter's details.

    Returns:
        A response object containing the status, message, and recruiter
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
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
