"""
This module provides views for the WorkExperience model in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.controllers.schemas import work_experience_schema
from server.controllers.work_experience_controller import WorkExperienceController
from server.exception import UnauthorizedError
from server.api.v1.views import app_views

# work_experience_views = Blueprint("work_experience_views", __name__)

work_experience_controller = WorkExperienceController()


@app_views.route("/work_experiences", methods=["POST"])
@jwt_required()
@swag_from("docs/app_views/create_work_experience.yaml")
def create_work_experience():
    """
    Creates a new work experience.

    Returns:
        A response object containing the status, message, and work experience
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        new_work_exp = work_experience_controller.create_work_experience(
            user_id, request.json
        )
        return (
            make_response_(
                "success",
                "WorkExperience created successfully",
                {"id": new_work_exp.id},
            ),
            201,
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@app_views.route(
        "/work_experiences/<work_experience_id>",
        methods=["GET"]
        )
@jwt_required()
@swag_from("docs/app_views/get_work_experience.yaml")
def get_work_experience(work_experience_id):
    """
    Fetches the details of a specific work experience.

    Returns:
        A response object containing the status, message, and work experience
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        work_experience = work_experience_controller.get_work_experiences(
            user_id, work_experience_id
        )
        return make_response_(
            "success",
            "WorkExperience details fetched successfully",
            {
                "id": work_experience.id,
                "title": work_experience.title,
                "description": work_experience.description,
            },
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 404


@app_views.route(
        "/work_experiences/<work_experience_id>",
        methods=["PUT"]
        )
@jwt_required()
@swag_from("docs/app_views/update_work_experience.yaml")
def update_work_experience(work_experience_id):
    """
    Updates the details of a specific work experience.

    Returns:
        A response object containing the status, message, and work experience
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        work_experience = work_experience_controller.update_work_experience(
            user_id, work_experience_id, request.json
        )
        return make_response_(
            "success",
            "WorkExperience details updated successfully",
            {
                "id": work_experience.id,
                "title": work_experience.title,
                "description": work_experience.description,
            },
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@app_views.route(
    "/work_experiences/<work_experience_id>", methods=["DELETE"]
)
@jwt_required()
@swag_from("docs/app_views/delete_work_experience.yaml")
def delete_work_experience(work_experience_id):
    """
    Deletes a specific work experience.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        work_experience_controller.delete_work_experience(
                user_id,
                work_experience_id
                )
        return make_response_("success", "WorkExperience deleted successfully")
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 404


@app_views.route("/work_experiences", methods=["GET"])
@app_views.route("/work_experiences/<major_id>", methods=["GET"])
@jwt_required()
@swag_from("docs/app_views/get_work_experiences.yaml")
def get_work_experiences(major_id=None):
    """
    Fetches all work experiences or work experiences related to a
    specific major.

    Returns:
        A list of all work experiences or work experiences related to a
        specific major in JSON format if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        work_experiences = work_experience_controller.get_work_experiences(
            user_id, major_id
        )
        work_experiences_data = [
            work_experience_schema.dump(work_experience)
            for work_experience in work_experiences
        ]
        return (
            make_response_(
                "success",
                "Fetched all work experiences",
                work_experiences_data
            ),
            200,
        )
    except UnauthorizedError as e:
        return make_response_("error", str(e)), 403
    except ValueError as e:
        return make_response_("error", str(e)), 404
