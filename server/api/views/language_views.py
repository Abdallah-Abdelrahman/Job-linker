"""
This module provides views for the Language model in the
Job-linker application.
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.controllers.language_controller import LanguageController
from server.controllers.schemas import language_schema
from server.exception import UnauthorizedError

language_views = Blueprint("language_views", __name__)

language_controller = LanguageController()


@language_views.route("/languages", methods=["GET"])
@jwt_required()
def get_languages():
    """
    Fetches all languages.

    Returns:
        A list of all languages in JSON format if successful.
        Otherwise, it returns an error message.
    """
    try:
        languages = language_controller.get_languages()
        languages_data = [
                language_schema.dump(language) for language in languages
                ]
        return jsonify(languages_data), 200
    except ValueError as e:
        return make_response_("error", str(e)), 404


@language_views.route("/languages", methods=["POST"])
@jwt_required()
def create_language():
    """
    Creates a new language.

    Returns:
        A response object containing the status, message, and language
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        new_language = language_controller.create_language(
                user_id,
                request.json
                )
        return (
            make_response_(
                "success",
                "Language created successfully",
                {"id": new_language.id},
            ),
            201,
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@language_views.route("/languages/<language_id>", methods=["PUT"])
@jwt_required()
def update_language(language_id):
    """
    Updates the details of a specific language.

    Returns:
        A response object containing the status, message, and language data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        language = language_controller.update_language(
            user_id, language_id, request.json
        )
        return make_response_(
            "success",
            "Language details updated successfully",
            {"id": language.id, "name": language.name},
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@language_views.route("/languages/<language_id>", methods=["DELETE"])
@jwt_required()
def delete_language(language_id):
    """
    Deletes a specific language.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        language_controller.delete_language(user_id, language_id)
        return make_response_("success", "Language deleted successfully")
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 404
