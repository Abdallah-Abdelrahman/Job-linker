from flask import Blueprint, jsonify, request, session
from flask_login import login_required
from marshmallow import ValidationError

from server.api.utils import make_response
from server.models import storage
from server.models.major import Major
from server.models.user import User

from .schemas import major_schema

major_views = Blueprint("major", __name__)


@major_views.route("/majors", methods=["GET"])
@login_required
def get_majors():
    majors = storage.all(Major).values()
    majors_data = [major_schema.dump(major) for major in majors]
    return jsonify(majors_data), 200


@major_views.route("/majors", methods=["POST"])
@login_required
def create_major():
    user = storage.get(User, session.get("user_id"))
    if not user or user.role != "recruiter":
        return make_response("error", "Unauthorized"), 401

    try:
        data = major_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    new_major = Major(name=data["name"])
    storage.new(new_major)
    storage.save()

    return (
        make_response(
            "success",
            "Major created successfully",
            {"id": new_major.id},
        ),
        201,
    )


@major_views.route("/majors/<major_id>", methods=["PUT"])
@login_required
def update_major(major_id):
    user = storage.get(User, session.get("user_id"))
    if not user or user.role != "recruiter":
        return make_response("error", "Unauthorized"), 401

    major = storage.get(Major, major_id)
    if not major:
        return make_response("error", "Major not found"), 404

    try:
        data = major_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    for key, value in data.items():
        setattr(major, key, value)
    storage.save()

    return make_response(
        "success",
        "Major details updated successfully",
        {"id": major.id, "name": major.name},
    )


@major_views.route("/majors/<major_id>", methods=["DELETE"])
@login_required
def delete_major(major_id):
    user = storage.get(User, session.get("user_id"))
    if not user or user.role != "recruiter":
        return make_response("error", "Unauthorized"), 401

    major = storage.get(Major, major_id)
    if not major:
        return make_response("error", "Major not found"), 404

    storage.delete(major)
    storage.save()

    return make_response(
        "success",
        "Major deleted successfully",
    )
