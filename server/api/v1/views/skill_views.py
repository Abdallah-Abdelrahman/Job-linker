"""
This module provides views for the Skill model in the Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.schemas import skill_schema
from server.controllers.skill_controller import SkillController
from server.decorators import handle_errors

skill_controller = SkillController()


@app_views.route("/skills", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_skills.yaml")
def get_skills():
    """
    Fetches all skills.

    Returns:
        A list of all skills in JSON format if successful.
        Otherwise, it returns an error message.
    """
    skills = skill_controller.get_skills()
    skills_data = [skill_schema.dump(skill) for skill in skills]
    return make_response_("success", "Fetched all skills", skills_data), 200


@app_views.route("/skills", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/create_skill.yaml")
def create_skill():
    """
    Creates a new skill.

    Returns:
        A response object containing the status, message, and skill data
        if successful.
        Otherwise, it returns an error message.
    """
    new_skill = skill_controller.create_skill(request.json)
    return (
        make_response_(
            "success",
            "Skill created successfully",
            {"id": new_skill.id},
        ),
        201,
    )


@app_views.route("/skills/<skill_id>", methods=["PUT"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/update_skill.yaml")
def update_skill(skill_id):
    """
    Updates the details of a specific skill.

    Returns:
        A response object containing the status, message, and skill data
        if successful.
        Otherwise, it returns an error message.
    """
    skill = skill_controller.update_skill(skill_id, request.json)
    return make_response_(
        "success",
        "Skill details updated successfully",
        {"id": skill.id, "name": skill.name},
    )


@app_views.route("/skills/<skill_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/delete_skill.yaml")
def delete_skill(skill_id):
    """
    Deletes a specific skill.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    skill_controller.delete_skill(skill_id)
    return make_response_("success", "Skill deleted successfully")
