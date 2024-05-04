"""Hanlde uploaded pdf files"""
import os
from datetime import datetime

from flasgger.utils import swag_from
from flask import request
from server.api.utils import make_response_
from server.config import ApplicationConfig
from werkzeug.utils import secure_filename
from server.api.v1.views import app_views


@app_views.route("/upload", methods=["POST"])
@swag_from("docs/app_views/upload.yaml")
def upload():
    """save file into server"""
    role = request.query_string.decode("utf8").split("=")[-1]

    # check if the post request has the file part
    if "file" not in request.files:
        return make_response_("No file part", "erro"), 400

    file = request.files["file"]
    extension = file.filename.split(".")[-1].lower()

    if not file or extension not in ApplicationConfig.ALLOWED_EXTENSIONS:
        return make_response_("Unsupported file type", "error"), 415

    filename = secure_filename(file.filename)
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_") + filename
    dir_ = {
        "candidate": ApplicationConfig.UPLOAD_CV,
        "recruiter": ApplicationConfig.UPLOAD_JOB,
    }
    file.save(
            os.path.join(
                dir_.get(role, ApplicationConfig.UPLOAD_CV),
                filename
                )
            )
    size = os.stat(
        os.path.join(dir_.get(role, ApplicationConfig.UPLOAD_CV), filename)
    ).st_size

    return make_response_(
            "uploaded successfully",
            "success",
            {"size": size}
            ), 201