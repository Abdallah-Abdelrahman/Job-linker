"""
This module provides a controller for the User model in the
Job-linker application.
"""

import os
from json import dumps, loads

from flask import current_app, url_for
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from marshmallow import ValidationError
from werkzeug.utils import secure_filename

from server.config import ApplicationConfig
from server.controllers.schemas import (
        login_schema,
        registration_schema,
        update_schema
        )
from server.email_templates import verification_email
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.recruiter import Recruiter
from server.models.user import User
from server.services.mail import MailService


class UserController:
    """
    Controller for User model.
    """

    def __init__(self, bcrypt_instance):
        """
        Initializes the UserController with a bcrypt instance for
        password hashing.
        """
        self.bcrypt = bcrypt_instance
        self.email_service = MailService()

    @classmethod
    def with_encrypt(cls):
        """Generate a new instance of UserController with encryption.

        Returns: new instance of UserController
        """
        from server.api.v1.app import app

        return UserController(Bcrypt(app))

    def get_user(self, user_id):
        """
        Gets a user by their ID.

        Args:
            user_id (int): The user's ID.

        Returns:
            The User object if they exist.

        Raises:
            ValueError: If the user is not found.
        """
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found.")
        return user

    def generate_verification_token(self, email):
        """
        Generates a unique verification token for a user's email.

        Args:
            email (str): The user's email address.

        Returns:
            str: The verification token.
        """
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(email, salt="email-verification")

    def send_verification_email(self, email, name, token):
        """
        Sends a verification email to the user.

        Args:
            email (str): The user's email address.
            token (str): The verification token.
        """
        template = verification_email(name, token)
        subject = "Email Verification for Joblinker"
        self.email_service.send_mail(template, email, name, subject)

    def verify_email(self, token):
        """
        Verifies a user's email.

        Args:
            token (str): The verification token.

        Raises:
            ValueError: If the token is invalid or expired.
        """
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            email = serializer.loads(
                token, salt="email-verification", max_age=3600)
        except (BadSignature, SignatureExpired):
            raise ValueError(
                "The verification link is invalid or has expired.")

        user = storage.get_by_attr(User, "email", email)
        if not user:
            raise ValueError("User not found.")

        user.verified = True
        storage.save()
        jwt = create_access_token(identity=user.id)
        jwt_refresh = create_refresh_token(identity=user.id)

        return jwt, jwt_refresh, user

    def register_user(self, data):
        """
        Registers a new user.

        Args:
            data: The data of the user to be registered.

        Returns:
            The registered user and their access token.

        Raises:
            ValueError: If there is a validation error or the user
            already exists.
        """
        # Validate data
        try:
            data = registration_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user already exists
        user = storage.get_by_attr(User, "email", data["email"])
        if user:
            raise ValueError("User already exists")

        # Create new user
        hashed_password = self.bcrypt.generate_password_hash(data["password"])
        new_user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password,
            role=data["role"],
            is_admin=data.get("is_admin", False),
        )
        storage.new(new_user)
        storage.save()

        return new_user

    def login_user(self, data):
        """
        Logs in a user.

        Args:
            data: The login data of the user.

        Returns:
            The logged in user and their access token.

        Raises:
            ValueError: If there is a validation error or the user does not
            exist or the password is incorrect.
        """
        # Validate data
        try:
            data = login_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user exists and password is correct and user is activated
        user = storage.get_by_attr(User, "email", data["email"])
        if not user or not self.bcrypt.check_password_hash(
            user.password, data["password"]
        ):
            raise ValueError("Unauthorized")

        if not user.verified:
            # Generate verification token
            verification_token = self.generate_verification_token(user.email)

            # Send verification email
            self.send_verification_email(
                user.email, user.name, verification_token)

            raise UnauthorizedError("Verify your email")
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return user, access_token, refresh_token

    def get_current_user(self, user_id):
        """
        Gets the current user.

        Args:
            user_id: The ID of the user.

        Returns:
            The current user.

        Raises:
            ValueError: If the user is unauthorized.
        """
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("User not found")

        user_data = user.to_dict
        if user_data.get("contact_info"):
            user_data["contact_info"] = loads(user_data.get("contact_info"))

        if user.role == "candidate":
            candidate = storage.get_by_attr(Candidate, "user_id", user_id)
            if not candidate:
                return user_data
            if candidate:
                user_data["candidate"] = {
                    "major": candidate.major.to_dict,
                    "skills": [skill.to_dict for skill in candidate.skills],
                    "languages": [
                        language.to_dict
                        for language in candidate.languages
                        ],
                    "applications": [
                        application.to_dict
                        for application in candidate.applications
                    ],
                    "experiences": [
                        experience.to_dict
                        for experience in candidate.experiences
                    ],
                    "education": [
                        education.to_dict
                        for education in candidate.educations
                    ],
                }
        elif user.role == "recruiter":
            recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
            if not recruiter:
                return user_data
            jobs = storage.get_all_by_attr(Job, "recruiter_id", recruiter.id)
            if recruiter:
                user_data["recruiter"] = {
                    "jobs": [job.to_dict for job in jobs],
                }

        # user_by_role = {'candidate': Candidate, 'recruiter': Recruiter}
        # instance = storage.get_by_attr(
        #               user_by_role.get(user.role),
        #               "user_id",
        #               user_id
        #               )

        # if instance:
        #     user_data.update(instance.to_dict)
        return user_data

    def update_current_user(self, user_id, data):
        """
        Updates the current user.

        Args:
            user_id: The ID of the user.
            data: The data to update the user with.

        Returns:
            The updated user.

        Raises:
            ValueError: If there is a validation error or the user is
            unauthorized.
        """
        ALLOWED_UPDATE_FIELDS = [
            "name",
            "profile_complete",
            "contact_info",
            "bio",
        ]

        # Validate data
        try:
            data = update_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Get user and update attributes
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("Unauthorized")

        for key, value in data.items():
            if key in ALLOWED_UPDATE_FIELDS:
                setattr(user, key, dumps(value) if key ==
                        "contact_info" else value)
            else:
                raise ValueError(f"Cannot update field: {key}")

        storage.save()
        return user

    def upload_profile_image(self, user_id, file):
        """
        Uploads a profile image for a user and updates
        their profile in the database.

        Args:
            user_id: The user's ID.
            file: The image file.

        Returns:
            A message, file path (if successful), and HTTP status code.
        """
        if (
            not file
            or "." not in file.filename
            or file.filename.rsplit(".", 1)[1].lower()
            not in ApplicationConfig.ALLOWED_IMAGE_EXTENSIONS
        ):
            return "Unsupported file type", None, 400

        if file.content_length > ApplicationConfig.MAX_IMAGE_CONTENT_LENGTH:
            return "File size exceeds the maximum limit", None, 400

        filename = secure_filename(file.filename)
        filename = f"{user_id}_{filename}"
        file_path = os.path.join(ApplicationConfig.UPLOAD_IMAGE, filename)
        file.save(file_path)

        # Update user profile with the image URL
        user = storage.get(User, user_id)
        if not user:
            return "User not found", None, 404

        # Generate the URL for the image
        image_url = url_for(
            "app_views.download_file",
            file_type="images",
            filename=filename,
            _external=True,
        )

        user.image_url = image_url
        storage.save()

        return (
            "Image uploaded successfully",
            {"file_path": file_path, "url": image_url},
            201,
        )

    def delete_current_user(self, user_id):
        """
        Deletes the current user.

        Args:
            user_id: The ID of the user.

        Raises:
            ValueError: If the user is unauthorized.
        """
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("Unauthorized")

        storage.delete(user)
        storage.save()

    def update_password(self, user_id, current_password, new_password):
        """
        Updates the password of the user.

        Args:
            user_id: The ID of the user.
            current_password: The current password of the user.
            new_password: The new password of the user.

        Returns:
            The updated user.

        Raises:
            ValueError: If there is a validation error or the user is
            unauthorized.
        """
        # Get user
        user = storage.get(User, user_id)
        if not user:
            raise ValueError("Unauthorized")

        # Check current password
        if not self.bcrypt.check_password_hash(
                user.password,
                current_password
                ):
            raise ValueError("Current password is incorrect")

        # Validate new password
        if not new_password or len(new_password) < 8:
            raise ValueError("New password is invalid")

        # Update password
        user.password = self.bcrypt.generate_password_hash(new_password)
        storage.save()

        return user
