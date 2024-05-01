"""
This module provides views for the Job model in the Job-linker application.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.controllers.job_controller import JobController
from server.controllers.schemas import job_schema
from server.exception import UnauthorizedError

job_views = Blueprint("job", __name__)

job_controller = JobController()


@job_views.route("/jobs", methods=["POST"])
@jwt_required()
def create_job():
    """
    Creates a new job.

    Returns:
        A response object containing the status, message, and job data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        new_job = job_controller.create_job(user_id, request.json)
        return (
            make_response_(
                "success",
                "Job created successfully",
                {"id": new_job.id},
            ),
            201,
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@job_views.route("/jobs/<job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):
    """
    Fetches the details of a specific job.

    Returns:
        A response object containing the status, message, and job data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        job = job_controller.get_job(user_id, job_id)
        return make_response_(
            "success",
            "Job details fetched successfully",
            {
                "id": job.id,
                "job_title": job.job_title,
                "job_description": job.job_description,
            },
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 404


@job_views.route("/jobs/<job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    """
    Updates the details of a specific job.

    Returns:
        A response object containing the status, message, and job data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        job = job_controller.update_job(user_id, job_id, request.json)
        return make_response_(
            "success",
            "Job details updated successfully",
            {
                "id": job.id,
                "job_title": job.job_title,
                "job_description": job.job_description,
            },
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@job_views.route("/jobs/<job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    """
    Deletes a specific job.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        job_controller.delete_job(user_id, job_id)
        return make_response_("success", "Job deleted successfully")
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 404


@job_views.route("/jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    """
    Fetches all jobs.

    Returns:
        A list of all jobs in JSON format if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        jobs = job_controller.get_jobs(user_id)
        jobs_data = [job_schema.dump(job) for job in jobs]
        return jsonify(jobs_data), 200
    except UnauthorizedError as e:
        return make_response_("error", str(e)), 403
    except ValueError as e:
        return make_response_("error", str(e)), 404


@job_views.route("/my_jobs", methods=["GET"])
@jwt_required()
def get_my_jobs():
    """
    Fetches all jobs created by the current user.

    Returns:
        A list of all jobs created by the current user in JSON format
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        jobs = job_controller.get_my_jobs(user_id)
        jobs_data = [job_schema.dump(job) for job in jobs]
        return jsonify(jobs_data), 200
    except UnauthorizedError as e:
        return make_response_("error", str(e)), 403
    except ValueError as e:
        return make_response_("error", str(e)), 404


@job_views.route("/jobs/<job_id>/recommended_candidates", methods=["GET"])
@jwt_required()
def get_recommended_candidates(job_id):
    """
    Fetch recommended candidates for a specific job.

    This endpoint returns a list of candidates that are recommended for
    the specified job based on the job's required skills and major. The
    user must be authenticated and have the role of a recruiter.

    Args:
        job_id: The ID of the job to fetch recommendations for.

    Returns:
        A JSON response containing the recommended candidates, or an error
        message if the candidates could not be fetched.
    """
    user_id = get_jwt_identity()
    try:
        # Fetch the recommended candidates
        rec_candidates = job_controller.recommend_candidates(job_id, user_id)

        # Convert the recommended candidates to JSON and return them
        return make_response_(
            "success",
            "Recommended Candidates based on Major & Skills",
            {"candidates": [
                candidate.to_dict for candidate in rec_candidates
                ]},
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400
