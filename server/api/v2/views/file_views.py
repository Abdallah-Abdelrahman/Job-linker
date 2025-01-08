"""Hanlde uploaded pdf files"""

import os
from datetime import datetime
from flask import Response, request

from server.api.utils import make_response_
from server.api.v2.views import app_views2
from server.config import ApplicationConfig
from server.decorators import handle_errors
from server.services.ai import AIService
from server.prompts import PTA_PROMPT


@app_views2.route("/cv-parse", methods=["POST"])
@handle_errors
def cv_parse():
    """Parse uploaded CV.
    Returns:
        json of cv data
    """
    # check if the post request has the file part
    if "file" not in request.files:
        return make_response_("error", "No file part"), 400

    file_path, original_filename = handle_upload(
        request.files["file"], f'{os.getcwd()}/pta'
    )
    ai = AIService(file_path=file_path)
    data = ai.to_dict(PTA_PROMPT)
    os.remove(file_path) # remove the file after parsing
    return make_response_("success", "parsed cv successfully!", data), 200


def handle_upload(file, directory):
    """Handle file upload and return file path and name.
    Ensure file extension, and prefix time to file name

    Args:
        file(Blob): file blob
        directory(str): directory to save the fle in
    """
    os.makedirs(directory, exist_ok=True) # if exist it's no-op
    extension = file.filename.split(".")[-1].lower()

    if not file or extension not in ApplicationConfig.ALLOWED_EXTENSIONS:
        raise ValueError("Unsupported file type")

    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_") + file.filename
    file_path = os.path.join(directory, filename)
    file.save(file_path)

    return file_path, file.filename
