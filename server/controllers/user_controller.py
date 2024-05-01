"""
This module provides a controller for the User model in the
Job-linker application.
"""

from flask import current_app, url_for
from flask_jwt_extended import create_access_token, create_refresh_token
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from marshmallow import ValidationError

from server.controllers.schemas import (
        login_schema,
        registration_schema,
        update_schema
        )
from server.exception import UnauthorizedError
from server.models import storage
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
        # verification_url = url_for(
        #         "user.verify_email",
        #         token=token,
        #         _external=True
        #         )
        "localhost:5173/verify?token={token}"
        html = (
                f"<p>Click the following link to verify your email:"
                f"<a href='http://localhost:5173/verify?token={token}'>"
                "Verify Email</a></p>"
                )

        self.email_service.send_mail(html, email, name)

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
                    token,
                    salt="email-verification",
                    max_age=3600
                    )
        except (BadSignature, SignatureExpired):
            raise ValueError(
                    "The verification link is invalid or has expired."
                    )

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
                    user.email,
                    user.name,
                    verification_token
                    )

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
            raise ValueError("Unauthorized")

        return user

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
            setattr(user, key, value)

        storage.save()
        return user

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
