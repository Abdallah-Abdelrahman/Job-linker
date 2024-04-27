from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from server.api.utils import make_response
from server.models import storage
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.recruiter import Recruiter

from .schemas import job_schema

job_views = Blueprint("job", __name__)


@job_views.route("/jobs", methods=["POST"])
@jwt_required()
def create_job():
    try:
        data = job_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user_id = get_jwt_identity()
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter:
        return make_response("error", "You are not a recruiter"), 403

    new_job = Job(
        recruiter_id=recruiter.id,
        major_id=data["major_id"],
        job_title=data["job_title"],
        job_description=data["job_description"],
        exper_years=data.get("exper_years"),
        salary=data.get("salary"),
    )
    storage.new(new_job)
    storage.save()

    return (
        make_response(
            "success",
            "Job created successfully",
            {"id": new_job.id},
        ),
        201,
    )


@job_views.route("/jobs/<job_id>", methods=["GET"])
@jwt_required()
def get_job(job_id):
    job = storage.get(Job, job_id)
    if not job:
        return make_response("error", "Job not found"), 404

    user_id = get_jwt_identity()
    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter or job.recruiter_id != recruiter.id:
        return make_response("error", "Unauthorized"), 401

    return make_response(
        "success",
        "Job details fetched successfully",
        {
            "id": job.id,
            "job_title": job.job_title,
            "job_description": job.job_description,
        },
    )


@job_views.route("/jobs/<job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    try:
        data = job_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    job = storage.get(Job, job_id)
    if not job:
        return make_response("error", "Job not found"), 404

    user_id = get_jwt_identity()
    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter or job.recruiter_id != recruiter.id:
        return make_response("error", "Unauthorized"), 401

    for key, value in data.items():
        setattr(job, key, value)
    storage.save()

    return make_response(
        "success",
        "Job details updated successfully",
        {
            "id": job.id,
            "job_title": job.job_title,
            "job_description": job.job_description,
        },
    )


@job_views.route("/jobs/<job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    job = storage.get(Job, job_id)
    if not job:
        return make_response("error", "Job not found"), 404

    user_id = get_jwt_identity()
    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter or job.recruiter_id != recruiter.id:
        return make_response("error", "Unauthorized"), 401

    storage.delete(job)
    storage.save()

    return make_response(
        "success",
        "Job deleted successfully",
    )


@job_views.route("/jobs", methods=["GET"])
@jwt_required()
def get_jobs():
    user_id = get_jwt_identity()
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    candidate = storage.get_by_attr(Candidate, "user_id", user_id)
    if not candidate:
        return make_response("error", "You are not a candidate"), 403

    major_id = candidate.major_id
    jobs = storage.get_all_by_attr(Job, "major_id", major_id)
    if not jobs:
        return make_response("error", "No jobs found for your major"), 404

    jobs_data = [job_schema.dump(job) for job in jobs]
    return jsonify(jobs_data), 200


@job_views.route("/my_jobs", methods=["GET"])
@jwt_required()
def get_my_jobs():
    user_id = get_jwt_identity()
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter:
        return make_response("error", "You are not a recruiter"), 403

    jobs = storage.get_all_by_attr(Job, "recruiter_id", recruiter.id)
    if not jobs:
        return make_response("error", "No jobs found"), 404

    jobs_data = [job_schema.dump(job) for job in jobs]
    return jsonify(jobs_data), 200
