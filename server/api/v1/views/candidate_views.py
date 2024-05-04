"""
This module provides views for the Candidate model in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.candidate_controller import CandidateController
from server.decorators import handle_errors

candidate_controller = CandidateController()


@app_views.route("/candidates", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/create_candidate.yaml")
def create_candidate():
    """
    Creates a new candidate.

    Returns:
        A response object containing the status, message, and
        candidate data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    new_candidate = candidate_controller.create_candidate(
            user_id,
            request.json
            )
    return (
        make_response_(
            "success",
            "Candidate created successfully",
            {"id": new_candidate.id},
        ),
        201,
    )


@app_views.route("/candidates/@me", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_current_candidate.yaml")
def get_current_candidate():
    """
    Fetches the current candidate's details.

    Returns:
        A response object containing the status, message, and
        candidate data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    candidate = candidate_controller.get_current_candidate(user_id)
    return make_response_(
        "success",
        "Candidate details fetched successfully",
        {
            "id": candidate.id,
            "major_id": candidate.major_id,
            "skills": [skill.id for skill in candidate.skills],
            "languages": [language.id for language in candidate.languages],
        },
    )


@app_views.route("/candidates/recommended_jobs", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_recommended_jobs.yaml")
def get_recommended_jobs():
    """
    Recommended jobs for the authenticated candidate.

    This endpoint returns a list of jobs that are recommended for the
    authenticated candidate based on their skills and major. The user
    must be authenticated and have the role of a candidate.

    Returns:
        A JSON response containing the recommended jobs, or an error
        message if the jobs could not be fetched.
    """
    user_id = get_jwt_identity()
    rec_jobs = candidate_controller.recommend_jobs(user_id)
    return make_response_(
        "success",
        "Recommended Jobs based on Major & Skills",
        {
            "jobs": [
                {"job": job["job"].to_dict, "has_applied": job["has_applied"]}
                for job in rec_jobs
            ]
        },
    )


@app_views.route("/candidates/@me", methods=["PUT"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/update_current_candidate.yaml")
def update_current_candidate():
    """
    Updates the current candidate's details.

    Returns:
        A response object containing the status, message, and candidate
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    candidate = candidate_controller.update_current_candidate(
            user_id,
            request.json
            )
    return make_response_(
        "success",
        "Candidate details updated successfully",
        {"id": candidate.id, "major_id": candidate.major_id},
    )


@app_views.route("/candidates/@me/skills", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/add_skill_to_current_candidate.yaml")
def add_skill_to_current_candidate():
    """
    Add a skill to the current candidate's profile.
    The skill ID should be provided in the request body.

    Returns:
        A success message and the updated list of skill IDs for the candidate.
    """
    user_id = get_jwt_identity()
    skill_id = request.json.get("skill_id")
    candidate = candidate_controller.add_skill(user_id, skill_id)
    return make_response_(
        "success",
        "Skill added successfully",
        {"id": candidate.id, "skills": [
            skill.id for skill in candidate.skills
            ]},
    )


@app_views.route("/candidates/@me/skills/<skill_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/remove_skill_from_current_candidate.yaml")
def remove_skill_from_current_candidate(skill_id):
    """
    Remove a skill from the current candidate's profile.
    The skill ID should be provided as a path parameter.

    Returns:
        A success message and the updated list of skill IDs for the candidate.
    """
    user_id = get_jwt_identity()
    candidate = candidate_controller.remove_skill(user_id, skill_id)
    return make_response_(
        "success",
        "Skill removed successfully",
        {"id": candidate.id, "skills": [
            skill.id for skill in candidate.skills
            ]},
    )


@app_views.route("/candidates/@me/languages", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/add_language_to_current_candidate.yaml")
def add_language_to_current_candidate():
    """
    Add a language to the current candidate's profile.
    The language ID should be provided in the request body.

    Returns:
        A success message and the updated list of language IDs for candidate.
    """
    user_id = get_jwt_identity()
    lang_id = request.json.get("lang_id")
    candidate = candidate_controller.add_language(user_id, lang_id)
    return make_response_(
        "success",
        "Language added successfully",
        {
            "id": candidate.id,
            "languages": [language.id for language in candidate.languages],
        },
    )


@app_views.route("/candidates/@me/languages/<lang_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/remove_language_from_current_candidate.yaml")
def remove_language_from_current_candidate(lang_id):
    """
    Remove a language from the current candidate's profile.
    The language ID should be provided as a path parameter.

    Returns:
        A success message and the updated list of language IDs for candidate.
    """
    user_id = get_jwt_identity()
    candidate = candidate_controller.remove_language(user_id, lang_id)
    return make_response_(
        "success",
        "Language removed successfully",
        {
            "id": candidate.id,
            "languages": [language.id for language in candidate.languages],
        },
    )


@app_views.route("/candidates/@me", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/delete_current_candidate.yaml")
def delete_current_candidate():
    """
    Deletes the current candidate.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    candidate_controller.delete_current_candidate(user_id)
    return make_response_("success", "Candidate profile deleted successfully")