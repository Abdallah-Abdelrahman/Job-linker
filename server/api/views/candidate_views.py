# Import necessary modules
from flask import Blueprint, request, session
from flask_login import login_required
from marshmallow import ValidationError
from server.api.utils import make_response
from server.models import storage
from server.models.candidate import Candidate

from .schemas import candidate_schema

candidate_views = Blueprint("candidate", __name__)


@candidate_views.route("/candidate", methods=["POST"])
@login_required
def create_candidate():
    """Create a new candidate."""
    try:
        data = candidate_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    user_id = session.get("user_id")
    if not user_id:
        return make_response("error", "Unauthorized"), 401

    new_candidate = Candidate(user_id=user_id, major_id=data["major_id"])
    storage.new(new_candidate)
    storage.save()

    return (
        make_response(
            "success", "Candidate created successfully", {"id": new_candidate.id}
        ),
        201,
    )


@candidate_views.route("/candidate/<can_id>", methods=["GET"])
@login_required
def get_candidate(can_id):
    """Get a candidate by ID."""
    candidate = storage.get(Candidate, can_id)
    if not candidate:
        return make_response("error", "Candidate not found"), 404

    return make_response(
        "success",
        "Candidate fetched successfully",
        {
            "id": candidate.id,
            "user_id": candidate.user_id,
            "major_id": candidate.major_id,
        },
    )


@candidate_views.route("/candidate/<can_id>", methods=["PUT"])
@login_required
def update_candidate(can_id):
    """Update a candidate's details."""
    try:
        data = candidate_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    candidate = storage.get(Candidate, can_id)
    if not candidate:
        return make_response("error", "Candidate not found"), 404

    for key, value in data.items():
        setattr(candidate, key, value)
    storage.save()

    return make_response(
        "success",
        "Candidate details updated successfully",
        {
            "id": candidate.id,
            "user_id": candidate.user_id,
            "major_id": candidate.major_id,
        },
    )


@candidate_views.route("/candidate/<can_id>", methods=["DELETE"])
@login_required
def delete_candidate(can_id):
    """Delete a candidate."""
    candidate = storage.get(Candidate, can_id)
    if not candidate:
        return make_response("error", "Candidate not found"), 404

    storage.delete(candidate)
    storage.save()

    return make_response("success", "Candidate deleted successfully")
