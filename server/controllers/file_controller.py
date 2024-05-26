"""
This module provides a controller for the file_views in the
Job-linker application.
"""

import os
from datetime import datetime

from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

from server.api.v1.app import app
from server.config import ApplicationConfig
from server.controllers.user_file_controller import UserFileController
from server.models import storage
from server.models.user import User
from server.prompts import ATS_FRIENDLY_PROMPT, CANDID_PROMPT, JOB_PROMPT
from server.services.ai import AIService
from server.services.ai_cand_creator import AICandidateProfileCreator
from server.services.ai_job_creator import AIJobCreator


class FileController:
    """
    Controller for handling operations related to file uploading.
    """

    def __init__(self):
        """
        Initialize the FileController.
        """
        self.user_file = UserFileController()
        self.bcrypt_instance = Bcrypt(app)

    def handle_upload(self, file, directory):
        """Handle file upload and return file path and name.
        Ensure file extension, and prefix time to file name

        Args:
            file(Blob): file blob
            directory(str): directory to save the fle in
        """
        extension = file.filename.split(".")[-1].lower()

        if not file or extension not in ApplicationConfig.ALLOWED_EXTENSIONS:
            raise ValueError("Unsupported file type")

        filename = secure_filename(file.filename)
        filename = datetime.now().strftime("%Y-%m-%d-%H-%M-%S_") + filename
        file_path = os.path.join(directory, filename)
        file.save(file_path)

        return file_path, file.filename

    def process_upload(
            self,
            file_path,
            original_filename,
            user_id,
            major_id=None
            ):
        """Process the uploaded file based on the user's role.
        It creates candidate profile or job from the uploaded file.
        """
        ai = AIService(pdf=file_path)

        # This logic will work with authorized or Unauthorized users
        user = storage.get(User, user_id)
        size = os.stat(file_path).st_size

        if user and user.role == "candidate":
            ai_data = ai.to_dict(CANDID_PROMPT)
            creator = AICandidateProfileCreator(
                user_id, ai_data, self.bcrypt_instance)
            candidate = creator.create_profile()
            new_file_path = os.path.join(
                ApplicationConfig.UPLOAD_CV,
                os.path.basename(file_path),
            )
            file_type = "cvs"
            os.rename(file_path, new_file_path)
            self.user_file.create_user_file(
                user_id, new_file_path, original_filename, file_type
            )
            return (
                "File uploaded and profile created successfully",
                {"size": size, "candidate_id": candidate.get("id")},
                201,
            )

        elif user and user.role == "recruiter":
            ai_data = ai.to_dict(JOB_PROMPT)
            ai_data["major_id"] = major_id
            creator = AIJobCreator(user_id, ai_data)
            job = creator.create_job()
            new_file_path = os.path.join(
                ApplicationConfig.UPLOAD_JOB,
                os.path.basename(file_path),
            )
            file_type = "jobs"
            os.rename(file_path, new_file_path)
            self.user_file.create_user_file(
                user_id, new_file_path, original_filename, file_type
            )
            return (
                "File uploaded and job created successfully",
                {"size": size, "job_id": job.id},
                201,
            )

        else:
            ai_data = ai.to_dict(CANDID_PROMPT)
            if os.path.exists(file_path):
                os.remove(file_path)
            return (
                "uploaded successfully",
                {
                    "size": size,
                    "ai_data": ai_data,
                },
                201,
            )

    def generate_insights(self, file_path):
        """Generate ATS insights for the uploaded file."""
        ai = AIService(pdf=file_path)
        ai_data = ai.to_dict(ATS_FRIENDLY_PROMPT)
        size = os.stat(file_path).st_size
        if os.path.exists(file_path):
            os.remove(file_path)
        return (
            "File uploaded and ATS insights generated successfully",
            {"size": size, "ats_insights": ai_data},
            200,
        )

    def count_files(self, directory):
        """Count the number of files in a directory."""
        num_files = len(
            [
                f
                for f in os.listdir(directory)
                if os.path.isfile(os.path.join(directory, f))
            ]
        )
        return "Count retrieved successfully", {"count": num_files}, 200
