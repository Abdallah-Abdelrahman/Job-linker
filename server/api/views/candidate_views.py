"""
This module provides views for the Candidate model in the
Job-linker application.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.controllers.candidate_controller import CandidateController
from server.exception import UnauthorizedError

candidate_views = Blueprint("candidate", __name__)

candidate_controller = CandidateController()


@candidate_views.route("/candidates", methods=["POST"])
@jwt_required()
def create_candidate():
    """
    Creates a new candidate.

    Returns:
        A response object containing the status, message, and
        candidate data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
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
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@candidate_views.route("/candidates/@me", methods=["GET"])
@jwt_required()
def get_current_candidate():
    """
    Fetches the current candidate's details.

    Returns:
        A response object containing the status, message, and
        candidate data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        candidate = candidate_controller.get_current_candidate(user_id)
        return make_response_(
            "success",
            "Candidate details fetched successfully",
            {
                "id": candidate.id,
                "major_id": candidate.major_id,
            },
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError:
        return make_response_("error", "Candidate not found"), 404


@candidate_views.route("/candidates/recommended_jobs", methods=["GET"])
@jwt_required()
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
    try:
        rec_jobs = candidate_controller.recommend_jobs(user_id)
        return make_response_(
            "success",
            "Recommended Jobs based on Major & Skills",
            {"jobs": [job.to_dict for job in rec_jobs]},
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@candidate_views.route("/candidates/@me", methods=["PUT"])
@jwt_required()
def update_current_candidate():
    """
    Updates the current candidate's details.

    Returns:
        A response object containing the status, message, and candidate
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        candidate = candidate_controller.update_current_candidate(
                user_id,
                request.json
                )
        return make_response_(
            "success",
            "Candidate details updated successfully",
            {"id": candidate.id, "major_id": candidate.major_id},
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@candidate_views.route("/candidates/@me", methods=["DELETE"])
@jwt_required()
def delete_current_candidate():
    """
    Deletes the current candidate.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        candidate_controller.delete_current_candidate(user_id)
        return make_response_(
                "success",
                "Candidate profile deleted successfully"
                )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError:
        return make_response_("error", "Candidate not found"), 404
