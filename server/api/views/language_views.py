from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.api.utils import make_response_
from server.models import storage
from server.models.language import Language
from server.models.user import User

from .schemas import language_schema

language_views = Blueprint("language_views", __name__)


@language_views.route("/languages", methods=["GET"])
@jwt_required()
def get_language():
    languages = storage.all(Language).values()
    languages_data = [language_schema.dump(language) for language in languages]
    return jsonify(languages_data), 200


@language_views.route("/languages", methods=["POST"])
@jwt_required()
def create_language():
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user or user.role != "recruiter":
        return make_response_("error", "Unautherized"), 400

    try:
        data = language_schema.load(request.json)
    except ValidationError as err:
        return make_response_("error", err.messages), 400

    new_language = Language(name=data["name"])
    storage.new(new_language)
    try:
        storage.save()
    except IntegrityError:
        return make_response_("error", "Language name already exists."), 409

    return (
        make_response_(
            "success", "Language created successfully", {"id": new_language.id}
        ),
        201,
    )


@language_views.route("/languages/<language_id>", methods=["PUT"])
@jwt_required()
def update_language(language_id):
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user or user.role != "recruiter":
        return make_response_("error", "Unautherized"), 401

    language = storage.get(Language, language_id)
    if not language:
        return make_response_("error", "Language not Found"), 404

    try:
        data = language_schema.load(request.json)
    except ValidationError as err:
        return make_response_("error", err.messages), 400

    for key, value in data.items():
        setattr(language, key, value)
    storage.save()

    return make_response_(
        "success",
        "Language Details updated successfully",
        {"id": language.id, "name": language.name},
    )


@language_views.route("/languages/<language_id>", methods=["DELETE"])
@jwt_required()
def delete_language(language_id):
    user_id = get_jwt_identity()
    user = storage.get(User, user_id)
    if not user or user.role != "recruiter":
        return make_response_("error", "Unautherized"), 401

    language = storage.get(Language, language_id)
    if not language:
        return make_response_("error", "Language not Found"), 404

    storage.delete(language)
    storage.save()

    return make_response_("success", "Language deleted successfully")
