from flask import Blueprint, request, session
from flask_login import login_required
from marshmallow import ValidationError

from server.api.utils import make_response
from server.models import storage
from server.models.recruiter import Recruiter

from .schemas import recruiter_schema

recruiter_views = Blueprint("recruiter", __name__)


@recruiter_views.route("/recruiters", methods=["POST"])
@login_required
def create_recruiter():
    try:
        data = recruiter_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user_id = session.get("user_id")
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    new_recruiter = Recruiter(
        user_id=user_id,
        company_name=data["company_name"],
        company_info=data.get("company_info"),
    )
    storage.new(new_recruiter)
    storage.save()

    return (
        make_response(
            "success",
            "Recruiter created successfully",
            {"id": new_recruiter.id},
        ),
        201,
    )


@recruiter_views.route("/recruiters/@me", methods=["GET"])
@login_required
def get_current_recruiter():
    user_id = session.get("user_id")
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter:
        return make_response("error", "Recruiter not found"), 404

    return make_response(
        "success",
        "Recruiter details fetched successfully",
        {
            "id": recruiter.id,
            "company_name": recruiter.company_name,
            "company_info": recruiter.company_info,
        },
    )


@recruiter_views.route("/recruiters/@me", methods=["PUT"])
@login_required
def update_current_recruiter():
    try:
        data = recruiter_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user_id = session.get("user_id")
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
    if not recruiter:
        return make_response("error", "Recruiter not found"), 404

    for key, value in data.items():
        setattr(recruiter, key, value)
    storage.save()

    return make_response(
        "success",
        "Recruiter details updated successfully",
        {
            "id": recruiter.id,
            "company_name": recruiter.company_name,
            "company_info": recruiter.company_info,
        },
    )
