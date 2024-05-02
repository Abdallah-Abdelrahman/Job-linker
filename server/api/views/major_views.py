"""
This module provides views for the Major model in the Job-linker application.
"""

from flasgger.utils import swag_from
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from server.api.utils import make_response_
from server.controllers.major_controller import MajorController
from server.controllers.schemas import major_schema
from server.exception import UnauthorizedError

major_views = Blueprint("major", __name__)

major_controller = MajorController()


@major_views.route("/majors", methods=["GET"])
@jwt_required()
@swag_from("docs/major_views/get_majors.yaml")
def get_majors():
    """
    Fetches all majors.

    Returns:
        A list of all majors in JSON format if successful.
        Otherwise, it returns an error message.
    """
    try:
        majors = major_controller.get_majors()
        majors_data = [major_schema.dump(major) for major in majors]
        return jsonify(majors_data), 200
    except ValueError as e:
        return make_response_("error", str(e)), 404


@major_views.route("/majors", methods=["POST"])
@jwt_required()
@swag_from("docs/major_views/create_major.yaml")
def create_major():
    """
    Creates a new major.

    Returns:
        A response object containing the status, message, and major
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        new_major = major_controller.create_major(user_id, request.json)
        return (
            make_response_(
                "success",
                "Major created successfully",
                {"id": new_major.id},
            ),
            201,
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@major_views.route("/majors/<major_id>", methods=["PUT"])
@jwt_required()
@swag_from("docs/major_views/update_major.yaml")
def update_major(major_id):
    """
    Updates the details of a specific major.

    Returns:
        A response object containing the status, message, and major
        data if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        major = major_controller.update_major(user_id, major_id, request.json)
        return make_response_(
            "success",
            "Major details updated successfully",
            {"id": major.id, "name": major.name},
        )
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 400


@major_views.route("/majors/<major_id>", methods=["DELETE"])
@jwt_required()
@swag_from("docs/major_views/delete_major.yaml")
def delete_major(major_id):
    """
    Deletes a specific major.

    Returns:
        A response object containing the status and message if successful.
        Otherwise, it returns an error message.
    """
    user_id = get_jwt_identity()
    try:
        major_controller.delete_major(user_id, major_id)
        return make_response_("success", "Major deleted successfully")
    except UnauthorizedError:
        return make_response_("error", "Unauthorized"), 401
    except ValueError as e:
        return make_response_("error", str(e)), 404
