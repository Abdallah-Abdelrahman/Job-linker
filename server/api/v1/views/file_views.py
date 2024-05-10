"""Hanlde uploaded pdf files"""
import os
from datetime import datetime

from flasgger.utils import swag_from
from flask import request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError
from werkzeug.utils import secure_filename

from server.api.utils import make_response_
from server.api.v1.views import app_views
from server.config import ApplicationConfig
from server.models import storage
from server.models.user import User
from server.prompts import ATS_FRIENDLY_PROMPT, CANDID_PROMPT
from server.services.ai import AIService
from server.services.ai_cand_creator import AICandidateProfileCreator


@app_views.route("/upload", methods=["POST"])
@swag_from("docs/app_views/upload.yaml")
def upload():
    """save file into server"""
    role = request.query_string.decode("utf8").split("=")[-1]
    dir_ = {
        "candidate": ApplicationConfig.UPLOAD_CV,
        "recruiter": ApplicationConfig.UPLOAD_JOB,
    }

    # check if the post request has the file part
    if "file" not in request.files:
        return make_response_("No file part", "error"), 400

    try:
        file_path, size = handle_upload(
            request.files["file"], dir_.get(role, ApplicationConfig.UPLOAD_CV)
        )
    except ValueError as e:
        return make_response_(str(e), "error"), 415

    # Parse the CV using AI service
    ai = AIService(pdf=file_path)
    ai_data = ai.to_dict(CANDID_PROMPT)

    # Try to get the user_id from the JWT
    # So this route will work with authorized or Unauthorized users
    user_id = None
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
    except NoAuthorizationError:
        pass

    if user_id is not None:
        user = storage.get(User, user_id)
        if user and user.role == "candidate":
            from server.api.v1.app import app

            bcrypt_instance = Bcrypt(app)
            creator = AICandidateProfileCreator(
                    user_id,
                    ai_data,
                    bcrypt_instance
                    )
            candidate = creator.create_profile()
            return (
                make_response_(
                    "File uploaded and profile created successfully",
                    "success",
                    {"size": size, "candidate_id": candidate.id},
                ),
                201,
            )

    return (
        make_response_(
            "uploaded successfully",
            "success",
            {"size": size, "ai_data": ai_data}
        ),
        201,
    )


@app_views.route("/upload/insights", methods=["POST"])
@swag_from("docs/app_views/upload_insights.yaml")
def upload_insights():
    """save file into server and return ATS insights"""
    # check if the post request has the file part
    if "file" not in request.files:
        return make_response_("No file part", "error"), 400

    try:
        file_path, size = handle_upload(
            request.files["file"], ApplicationConfig.UPLOAD_CV
        )
    except ValueError as e:
        return make_response_(str(e), "error"), 415

    # Parse the CV using AI service
    ai = AIService(pdf=file_path)
    ai_data = ai.get_cv_insights(ATS_FRIENDLY_PROMPT)

    return (
        make_response_(
            "File uploaded and ATS insights generated successfully",
            "success",
            {"size": size, "ats_insights": ai_data},
        ),
        201,
    )


def handle_upload(file, directory):
    """Handle file upload and return file path and size."""
    extension = file.filename.split(".")[-1].lower()

    if not file or extension not in ApplicationConfig.ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    filename = secure_filename(file.filename)
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_") + filename
    file_path = os.path.join(directory, filename)
    file.save(file_path)
    size = os.stat(file_path).st_size

    return file_path, size


@app_views.route("/count/cv", methods=["GET"])
@swag_from("docs/app_views/count_cv_files.yaml")
def count_cv_files():
    """Return the count of uploaded CV files"""
    cv_dir = ApplicationConfig.UPLOAD_CV
    num_files = len(
        [
            f for f in os.listdir(cv_dir)
            if os.path.isfile(os.path.join(cv_dir, f))
            ]
    )
    return (
        make_response_(
            "Count retrieved successfully",
            "success",
            {"count": num_files}),
        200,
    )


@app_views.route("/count/job", methods=["GET"])
@swag_from("docs/app_views/count_job_files.yaml")
def count_job_files():
    """Return the count of uploaded job description files"""
    job_dir = ApplicationConfig.UPLOAD_JOB
    num_files = len(
        [
            f for f in os.listdir(job_dir)
            if os.path.isfile(os.path.join(job_dir, f))
            ]
    )
    return (
        make_response_(
            "Count retrieved successfully",
            "success",
            {"count": num_files}),
        200,
    )
