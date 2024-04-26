from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from marshmallow import ValidationError

from server.api.utils import make_response
from server.models import storage
from server.models.candidate import Candidate
from server.models.work_experience import WorkExperience

from .schemas import work_experience_schema

work_experience_views = Blueprint("work_experience_views", __name__)


@work_experience_views.route("/work_experiences", methods=["GET"])
@login_required
def get_work_experiences():
    if current_user.role == "recruiter":
        work_experiences = storage.all(WorkExperience).values()
    elif current_user.candidate is not None:
        work_experiences = current_user.candidate.experiences
    else:
        return (
            make_response(
                "error", "The current user does not have a candidate profile"
            ),
            400,
        )

    work_experiences_data = [
        work_experience_schema.dump(work_experience)
        for work_experience in work_experiences
    ]
    return jsonify(work_experiences_data), 200


@work_experience_views.route("/work_experiences", methods=["POST"])
@login_required
def create_work_experience():
    if current_user.role != "candidate":
        return (
            make_response(
                "error", "Only candidates can add work experiences"
            ),
            403,
        )

    if current_user.candidate is None:
        return (
            make_response(
                "error", "The current user does not have a candidate profile"
            ),
            400,
        )

    try:
        data = work_experience_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    new_work_experience = WorkExperience(
            candidate_id=current_user.candidate.id, **data
            )
    storage.new(new_work_experience)
    storage.save()

    return (
        make_response(
            "success",
            "WorkExperience created successfully",
            {"id": new_work_experience.id},
        ),
        201,
    )


@work_experience_views.route(
        "/work_experiences/<work_experience_id>",
        methods=["PUT"]
        )
@login_required
def update_work_experience(work_experience_id):
    work_experience = storage.get(WorkExperience, work_experience_id)
    if not work_experience:
        return make_response("error", "WorkExperience not found"), 404

    if work_experience.candidate_id != current_user.candidate.id:
        return (
            make_response(
                "error",
                "You can only update your own work experiences"
                ),
            403,
        )

    try:
        data = work_experience_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    for key, value in data.items():
        setattr(work_experience, key, value)
    storage.save()

    return make_response(
        "success",
        "WorkExperience details updated successfully",
        {"id": work_experience.id, "title": work_experience.title},
    )


@work_experience_views.route(
    "/work_experiences/<work_experience_id>", methods=["DELETE"]
)
@login_required
def delete_work_experience(work_experience_id):
    work_experience = storage.get(WorkExperience, work_experience_id)
    if not work_experience:
        return make_response("error", "WorkExperience not found"), 404

    if work_experience.candidate_id != current_user.candidate.id:
        return (
            make_response(
                "error",
                "You can only delete your own work experiences"
                ),
            403,
        )

    storage.delete(work_experience)
    storage.save()

    return make_response(
        "success",
        "WorkExperience deleted successfully",
    )
