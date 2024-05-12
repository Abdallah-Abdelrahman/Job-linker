"""
This module provides views for the Application model in the
Job-linker application.
"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.controllers.application_controller import ApplicationsController
from server.controllers.schemas import application_schema
from server.decorators import handle_errors

applications_controller = ApplicationsController()


@app_views.route("/applications", methods=["POST"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/create_application.yaml")
def create_application():
    """
    Create a new job application.

    This endpoint allows a user to create a new job application. The user
    must be authenticated,
    and the request data must contain the details of the application.

    Returns:
        A JSON response containing the details of the created application,
        or an error message if the application could not be created.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    application = applications_controller.create_application(user_id, data)
    return (
        make_response_(
            "success",
            "Application created successfully",
            application_schema.dump(application),
        ),
        201,
    )


@app_views.route("/applications/<application_id>", methods=["PUT"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/update_application.yaml")
def update_application(application_id):
    """
    Update an existing job application.

    This endpoint allows a user to update an existing job application. The user
    must be authenticated recruiter,
    and the request data must contain the updated details of the application.

    Args:
        application_id: The ID of the application to update.

    Returns:
        A JSON response containing the details of the updated application,
        or an error message if the application could not be updated.
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    application = applications_controller.update_application(
        user_id, application_id, data
    )
    return (
        make_response_(
            "success",
            "Application updated successfully",
            application_schema.dump(application),
        ),
        200,
    )


@app_views.route(
        "/applications",
        defaults={"application_id": None},
        methods=["GET"]
        )
@app_views.route("/applications/<application_id>", methods=["GET"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/get_application.yaml")
def get_application(application_id):
    """
    Fetch one or all job applications.

    This endpoint allows a user to fetch the details of one or all job
    applications. The user must be authenticated. If an application ID
    is provided, the details of that specific application are returned.
    If no application ID is provided, the details of all applications
    are returned.

    Args:
        application_id: The ID of the application to fetch. If None,
        all applications are fetched.

    Returns:
        A JSON response containing the details of the fetched application(s),
        or an error message if the application(s) could not be fetched.
    """
    user_id = get_jwt_identity()
    application = applications_controller.get_application(
            user_id,
            application_id
            )
    return (
        make_response_(
            "success",
            "Application fetched successfully",
            application,
        ),
        200,
    )


@app_views.route("/applications/<application_id>", methods=["DELETE"])
@jwt_required()
@handle_errors
@swag_from("docs/app_views/delete_application.yaml")
def delete_application(application_id):
    """
    Delete a job application.

    This endpoint allows a user to delete a job application. The user must
    be authenticated, and the ID of the application to delete must be provided.

    Args:
        application_id: The ID of the application to delete.

    Returns:
        A JSON response containing a success message if the application was
        deleted successfully, or an error message if the application could
        not be deleted.
    """
    user_id = get_jwt_identity()
    applications_controller.delete_application(user_id, application_id)
    return make_response_("success", "Application deleted successfully"), 200


@app_views.route("/applications/hired_count", methods=["GET"])
@swag_from("docs/app_views/get_hired_count.yaml")
def get_hired_count():
    """
    Fetches the count of hired candidates.

    Returns:
        The count of hired candidates.
    """
    count = applications_controller.get_hired_count()
    return (
        make_response_(
            "success", "Fetched count of hired candidates", {"count": count}
        ),
        200,
    )
