"""
This module provides views for the Language model in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.language_controller import LanguageController
from server.controllers.schemas import language_schema
from server.decorators import handle_errors

language_controller = LanguageController()


@app_views.route("/languages", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_languages.yaml")
def get_languages():
    """
    Fetches all languages.

    Returns:
        A list of all languages in JSON format if successful.
        Otherwise, it returns an error message.
    """
    languages = language_controller.get_languages()
    languages_data = [language_schema.dump(language) for language in languages]
    return make_response_(
            "success",
            "Fetched all languages",
            languages_data
            ), 200


@app_views.route("/languages", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/create_language.yaml")
def create_language():
    """
    Creates a new language.

    Returns:
        A response object containing the status, message, and language
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    new_language = language_controller.create_language(user_id, request.json)
    return (
        make_response_(
            "success",
            "Language created successfully",
            {"id": new_language.id},
        ),
        201,
    )


@app_views.route("/languages/<language_id>", methods=["PUT"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/update_language.yaml")
def update_language(language_id):
    """
    Updates the details of a specific language.

    Returns:
        A response object containing the status, message, and language data
        if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    language = language_controller.update_language(
            user_id,
            language_id,
            request.json
            )
    return make_response_(
        "success",
        "Language details updated successfully",
        {"id": language.id, "name": language.name},
    )


@app_views.route("/languages/<language_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/delete_language.yaml")
def delete_language(language_id):
    """
    Deletes a specific language.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    language_controller.delete_language(user_id, language_id)
    return make_response_("success", "Language deleted successfully")
