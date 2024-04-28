"""
This module provides views for the Skill model in the Job-linker application.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from server.api.utils import make_response_
from server.controllers.schemas import skill_schema
from server.controllers.skill_controller import SkillController

skill_views = Blueprint("skill", __name__)

skill_controller = SkillController()


@skill_views.route("/skills", methods=["GET"])
@jwt_required()
def get_skills():
    """
    Fetches all skills.

    Returns:
        A list of all skills in JSON format if successful.
        Otherwise, it returns an error message.
    """
    try:
        skills = skill_controller.get_skills()
        skills_data = [skill_schema.dump(skill) for skill in skills]
        return jsonify(skills_data), 200
    except ValueError as e:
        return make_response_("error", str(e)), 404


@skill_views.route("/skills", methods=["POST"])
@jwt_required()
def create_skill():
    """
    Creates a new skill.

    Returns:
        A response object containing the status, message, and skill data
        if successful.
        Otherwise, it returns an error message.
    """
    try:
        new_skill = skill_controller.create_skill(request.json)
        return (
            make_response_(
                "success",
                "Skill created successfully",
                {"id": new_skill.id},
            ),
            201,
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400


@skill_views.route("/skills/<skill_id>", methods=["PUT"])
@jwt_required()
def update_skill(skill_id):
    """
    Updates the details of a specific skill.

    Returns:
        A response object containing the status, message, and skill data
        if successful.
        Otherwise, it returns an error message.
    """
    try:
        skill = skill_controller.update_skill(skill_id, request.json)
        return make_response_(
            "success",
            "Skill details updated successfully",
            {"id": skill.id, "name": skill.name},
        )
    except ValueError as e:
        return make_response_("error", str(e)), 400


@skill_views.route("/skills/<skill_id>", methods=["DELETE"])
@jwt_required()
def delete_skill(skill_id):
    """
    Deletes a specific skill.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    try:
        skill_controller.delete_skill(skill_id)
        return make_response_("success", "Skill deleted successfully")
    except ValueError as e:
        return make_response_("error", str(e)), 404
