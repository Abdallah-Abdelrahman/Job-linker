"""
This module provides views for the Job model in the Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.job_controller import JobController
from server.controllers.schemas import job_schema
from server.decorators import handle_errors

job_controller = JobController()


@app_views.route("/jobs", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/create_job.yaml")
def create_job():
    """
    Creates a new job.

    Returns:
        A response object containing the status, message, and job data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    new_job = job_controller.create_job(user_id, request.json)
    return (
        make_response_(
            "success",
            "Job created successfully",
            {"id": new_job.id},
        ),
        201,
    )


@app_views.route("/jobs/<job_id>", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_job.yaml")
def get_job(job_id):
    """
    Fetches the details of a specific job.

    Returns:
        A response object containing the status, message, and job data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
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


@app_views.route("/jobs/<job_id>", methods=["PUT"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/update_job.yaml")
def update_job(job_id):
    """
    Updates the details of a specific job.

    Returns:
        A response object containing the status, message, and job data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
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


@app_views.route("/jobs/<job_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/delete_job.yaml")
def delete_job(job_id):
    """
    Deletes a specific job.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    job_controller.delete_job(user_id, job_id)
    return make_response_("success", "Job deleted successfully")


@app_views.route("/jobs/<job_id>/skills", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/add_skill_to_job.yaml")
def add_skill_to_job(job_id):
    """
    Add a skill to a job.
    The job ID should be provided as a path parameter and the skill ID
    should be provided in the request body.

    Returns:
        A success message and the updated list of skill IDs for the job.
    """
    user_id = get_jwt_identity()
    skill_id = request.json.get("skill_id")
    job = job_controller.add_skill(user_id, job_id, skill_id)
    return make_response_(
        "success",
        "Skill added successfully",
        {"id": job.id, "skills": [skill.id for skill in job.skills]},
    )


@app_views.route("/jobs/<job_id>/skills/<skill_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/remove_skill_from_job.yaml")
def remove_skill_from_job(job_id, skill_id):
    """
    Remove a skill from a job.
    The job ID and skill ID should be provided as path parameters.

    Returns:
        A success message and the updated list of skill IDs for the job.
    """
    user_id = get_jwt_identity()
    job = job_controller.remove_skill(user_id, job_id, skill_id)
    return make_response_(
        "success",
        "Skill removed successfully",
        {"id": job.id, "skills": [skill.id for skill in job.skills]},
    )


@app_views.route("/jobs", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_jobs.yaml")
def get_jobs():
    """
    Fetches all jobs.

    If the user is a candidate, it returns all jobs for their major.
    If the user is a recruiter, it returns all jobs posted by them.

    Returns:
        A list of all jobs in JSON format if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    jobs = job_controller.get_jobs(user_id)
    jobs_data = [job_schema.dump(job) for job in jobs]
    return make_response_("success", "Fetched jobs", jobs_data), 200


@app_views.route("/jobs/<job_id>/recommended_candidates", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_recommended_candidates.yaml")
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
    rec_candidates = job_controller.recommend_candidates(job_id, user_id)

    return make_response_(
        "success",
        "Recommended Candidates based on Major & Skills",
        {"candidates": [candidate.to_dict for candidate in rec_candidates]},
    )