"""Hanlde uploaded pdf files"""

import mimetypes
import os

from flasgger.utils import swag_from
from flask import make_response, request, send_from_directory, url_for
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import NotFound

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.config import ApplicationConfig
from server.controllers.file_controller import FileController
from server.decorators import handle_errors
from server.extensions import limiter

file_controller = FileController()


@app_views.route("/upload", methods=["POST"])
@jwt_required(optional=True)
@handle_errors
@swag_from("docs/app_views/upload.yaml")
def upload():
    """save file into server"""
    role = request.query_string.decode("utf8").split("=")[-1]
    dir_ = {
        "candidate": ApplicationConfig.UPLOAD_CV,
        "recruiter": ApplicationConfig.UPLOAD_JOB,
        "visitor": ApplicationConfig.UPLOAD_TEMP,
    }

    # check if the post request has the file part
    if "file" not in request.files:
        return make_response_("error", "No file part"), 400

    major_id = request.form.get("major_id", None)

    file_path, original_filename = file_controller.handle_upload(
        request.files["file"], dir_.get(role, ApplicationConfig.UPLOAD_TEMP)
    )
    user_id = get_jwt_identity()
    message, data, status_code = file_controller.process_upload(
        file_path, original_filename, user_id, major_id
    )
    return make_response_("success", message, data), status_code


@app_views.route("/upload/insights", methods=["POST"])
@handle_errors
@limiter.limit("3 per minute")
@swag_from("docs/app_views/upload_insights.yaml")
def upload_insights():
    """save file into server and return ATS insights"""
    # check if the post request has the file part
    if "file" not in request.files:
        return make_response_("error", "No file part"), 400

    file_path, original_filename = file_controller.handle_upload(
        request.files["file"], ApplicationConfig.UPLOAD_CV
    )
    message, data, status_code = file_controller.generate_insights(file_path)
    return make_response_("success", message, data), status_code


@app_views.route("/count/cv", methods=["GET"])
@handle_errors
@swag_from("docs/app_views/count_cv_files.yaml")
def count_cv_files():
    """Return the count of uploaded CV files"""
    message, data, status_code = file_controller.count_files(
        ApplicationConfig.UPLOAD_CV
    )
    return make_response_("success", message, data), status_code


@app_views.route("/uploads/<file_type>/<filename>")
@jwt_required()
@handle_errors
def uploaded_file(file_type, filename):
    """
    Returns a URL that points to the user-uploaded file based
    on file type and name.

    Args:
        file_type (str): 'images', 'cvs', or 'jobs'.
        filename (str): Name of the file.

    Returns:
        URL to the file or error message in JSON format.
    """
    if file_type not in ["images", "cvs", "jobs"]:
        return make_response_("error", "Invalid file type", {}), 404

    directory = None
    if file_type == "images":
        directory = os.path.abspath(ApplicationConfig.UPLOADED_IMAGE_DEST)
    elif file_type == "cvs":
        directory = os.path.abspath(ApplicationConfig.UPLOADED_CV_DEST)
    elif file_type == "jobs":
        directory = os.path.abspath(ApplicationConfig.UPLOADED_JOB_DEST)

    if directory:
        try:
            # Check if the file exists
            if os.path.isfile(os.path.join(directory, filename)):
                # Return a URL that points to the file
                return make_response_(
                    "success",
                    "File found",
                    {
                        "url": url_for(
                            "app_views.download_file",
                            file_type=file_type,
                            filename=filename,
                            _external=True,
                        )
                    },
                )
            else:
                return make_response_("error", "File not found", {}), 404
        except NotFound:
            return make_response_("error", "File not found", {}), 404
    else:
        return make_response_("error", "Invalid file type", {}), 404


@app_views.route("/download/<file_type>/<filename>")
@handle_errors
def download_file(file_type, filename):
    """
    Serves user-uploaded files based on file type and name.

    Args:
        file_type (str): 'images', 'cvs', or 'jobs'.
        filename (str): Name of the file.

    Returns:
        File to be served or error message in JSON format.
    """
    if file_type not in ["images", "cvs", "jobs"]:
        return make_response_("error", "Invalid file type", {}), 404

    directory = None
    if file_type == "images":
        directory = os.path.abspath(ApplicationConfig.UPLOADED_IMAGE_DEST)
    elif file_type == "cvs":
        directory = os.path.abspath(ApplicationConfig.UPLOADED_CV_DEST)
    elif file_type == "jobs":
        directory = os.path.abspath(ApplicationConfig.UPLOADED_JOB_DEST)

    if directory:
        try:
            # Get the file path
            file_path = os.path.join(directory, filename)
            # Determine the MIME type of the file
            mime_type = mimetypes.guess_type(file_path)[0]
            # Send the file with the correct MIME type
            response = make_response(send_from_directory(directory, filename))
            response.headers.set("Content-Type", mime_type)
            return response
        except NotFound:
            return make_response_("error", "File not found", {}), 404
    else:
        return make_response_("error", "Invalid file type", {}), 404


@app_views.route("/count/job", methods=["GET"])
@handle_errors
@swag_from("docs/app_views/count_job_files.yaml")
def count_job_files():
    """Return the count of uploaded job description files"""
    message, data, status_code = file_controller.count_files(
        ApplicationConfig.UPLOAD_JOB
    )
    return make_response_("success", message, data), status_code
