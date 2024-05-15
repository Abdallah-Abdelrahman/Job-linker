"""Hanlde uploaded pdf files"""

from flasgger.utils import swag_from
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.config import ApplicationConfig
from server.controllers.file_controller import FileController
from server.decorators import handle_errors

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

    major_id = request.form.get('major_id', None)

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


@app_views.route("/count/job", methods=["GET"])
@handle_errors
@swag_from("docs/app_views/count_job_files.yaml")
def count_job_files():
    """Return the count of uploaded job description files"""
    message, data, status_code = file_controller.count_files(
        ApplicationConfig.UPLOAD_JOB
    )
    return make_response_("success", message, data), status_code
