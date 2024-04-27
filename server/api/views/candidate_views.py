from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from server.api.utils import make_response_
from server.models import storage
from server.models.candidate import Candidate
from server.models.user import User

from .schemas import candidate_schema

candidate_views = Blueprint("candidate", __name__)


@candidate_views.route("/candidates", methods=["POST"])
@jwt_required()
def create_candidate():
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user or user.role != "candidate":
        return make_response_("error", "Unauthorized"), 401

    try:
        data = candidate_schema.load(request.json)
    except ValidationError as err:
        return make_response_("error", err.messages), 400

    new_candidate = Candidate(
        user_id=user_id,
        major_id=data["major_id"],
    )
    storage.new(new_candidate)
    storage.save()

    return (
        make_response_(
            "success",
            "Candidate created successfully",
            {"id": new_candidate.id},
        ),
        201,
    )


@candidate_views.route("/candidates/@me", methods=["GET"])
@jwt_required()
def get_current_candidate():
    user_id = get_jwt_identity()
    if not user_id:
        return make_response_("error", "Unauthorized"), 401

    candidate = storage.get_by_attr(Candidate, "user_id", user_id)
    if not candidate:
        return make_response_("error", "Candidate not found"), 404

    return make_response_(
        "success",
        "Candidate details fetched successfully",
        {
            "id": candidate.id,
            "major_id": candidate.major_id,
        },
    )


@candidate_views.route("/candidates/@me", methods=["PUT"])
@jwt_required()
def update_current_candidate():
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user or user.role != "candidate":
        return make_response_("error", "Unauthorized"), 401

    candidate = storage.get_by_attr(Candidate, "user_id", user_id)
    if not candidate:
        return make_response_("error", "Candidate not found"), 404

    try:
        data = candidate_schema.load(request.json)
    except ValidationError as err:
        return make_response_("error", err.messages), 400

    for key, value in data.items():
        setattr(candidate, key, value)
    storage.save()

    return make_response_(
        "success",
        "Candidate details updated successfully",
        {"id": candidate.id, "major_id": candidate.major_id},
    )


@candidate_views.route("/candidates/@me", methods=["DELETE"])
@jwt_required()
def delete_current_candidate():
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user or user.role != "candidate":
        return make_response_("error", "Unauthorized"), 401

    candidate = storage.get_by_attr(Candidate, "user_id", user_id)
    if not candidate:
        return make_response_("error", "Candidate not found"), 404

    storage.delete(candidate)
    storage.save()

    return make_response_("success", "Candidate profile deleted successfully")
