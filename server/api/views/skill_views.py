from flask import Blueprint, jsonify, request
from flask_login import login_required
from marshmallow import ValidationError

from server.api.utils import make_response
from server.models import storage
from server.models.skill import Skill

from .schemas import skill_schema

skill_views = Blueprint("skill", __name__)


@skill_views.route("/skills", methods=["GET"])
@login_required
def get_skills():
    skills = storage.all(Skill).values()
    skills_data = [skill_schema.dump(skill) for skill in skills]
    return jsonify(skills_data), 200


@skill_views.route("/skills", methods=["POST"])
@login_required
def create_skill():
    try:
        data = skill_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    new_skill = Skill(name=data["name"])
    storage.new(new_skill)
    storage.save()

    return (
        make_response(
            "success",
            "Skill created successfully",
            {"id": new_skill.id},
        ),
        201,
    )


@skill_views.route("/skills/<skill_id>", methods=["PUT"])
@login_required
def update_skill(skill_id):
    skill = storage.get(Skill, skill_id)
    if not skill:
        return make_response("error", "Skill not found"), 404

    try:
        data = skill_schema.load(request.json)
    except ValidationError as err:
        return make_response("error", err.messages), 400

    for key, value in data.items():
        setattr(skill, key, value)
    storage.save()

    return make_response(
        "success",
        "Skill details updated successfully",
        {"id": skill.id, "name": skill.name},
    )


@skill_views.route("/skills/<skill_id>", methods=["DELETE"])
@login_required
def delete_skill(skill_id):
    skill = storage.get(Skill, skill_id)
    if not skill:
        return make_response("error", "Skill not found"), 404

    storage.delete(skill)
    storage.save()

    return make_response(
        "success",
        "Skill deleted successfully",
    )
