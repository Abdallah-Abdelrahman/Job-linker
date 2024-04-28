"""
This module provides a controller for the User model in the
Job-linker application.
"""

from flask_jwt_extended import create_access_token
from marshmallow import ValidationError

from server.controllers.schemas import (
        login_schema,
        registration_schema,
        update_schema
        )
from server.models import storage
from server.models.user import User


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
        )
        storage.new(new_user)
        storage.save()

        access_token = create_access_token(identity=new_user.id)
        return new_user, access_token

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

        # Check if user exists and password is correct
        user = storage.get_by_attr(User, "email", data["email"])
        if not user or not self.bcrypt.check_password_hash(
            user.password, data["password"]
        ):
            raise ValueError("Unauthorized")

        access_token = create_access_token(identity=user.id)
        return user, access_token

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
