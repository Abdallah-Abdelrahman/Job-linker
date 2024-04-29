'''Hanlde uploaded pdf files'''
import os
from datetime import datetime
from flask import Blueprint,  request
from werkzeug.utils import secure_filename
from server.config import ApplicationConfig
from server.api.utils import make_response_

file_views = Blueprint("file", __name__)


@file_views.route('/upload', methods=['POST'])
def upload():
    '''save file into server'''
    # check if the post request has the file part
    role = request.query_string.decode('utf8').split('=')[-1]

    if 'file' not in request.files:
        return make_response_('No file part', 'erro'), 400

    file = request.files['file']
    extension = file.filename.split('.')[-1].lower()

    if not file or extension not in ApplicationConfig.ALLOWED_EXTENSIONS:
        return make_response_('Unsupported file type', 'error'), 415

    filename = secure_filename(file.filename)
    filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_") + filename
    dir_ = {
            'candidate': ApplicationConfig.UPLOAD_CV,
            'recruiter': ApplicationConfig.UPLOAD_JOB
    }
    file.save(os.path.join(
        dir_.get(role, ApplicationConfig.UPLOAD_CV), filename)
    )
    size = os.stat(os.path.join(dir_.get(role, ApplicationConfig.UPLOAD_CV),
                                filename)).st_size

    return make_response_('uploaded successfully', 'success',
                          {'size': size}), 201
