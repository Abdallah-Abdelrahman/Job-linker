"""
This module provides a controller for the Major model in the
Job-linker application.
"""

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.controllers.schemas import major_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.major import Major
from server.models.user import User


class MajorController:
    """
    Controller for Major model.
    """

    def __init__(self):
        """
        Initializes the MajorController.
        """
        pass

    def get_majors(self):
        """
        Fetches all majors.

        Returns:
            A list of all majors.
        """
        majors = storage.all(Major).values()
        return majors

    def create_major(self, user_id, data):
        """
        Creates a new major.

        Args:
            user_id: The ID of the user.
            data: The data of the major to be created.

        Returns:
            The created major.

        Raises:
            ValueError: If there is a validation error or the major
            name already exists.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Validate data
        try:
            data = major_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        user = storage.get(User, user_id)
        # if not user or user.role != "recruiter":
        #     raise UnauthorizedError("Unauthorized")

        # Create new major
        new_major = Major(name=data["name"])
        storage.new(new_major)
        try:
            storage.save()
        except IntegrityError:
            raise ValueError("Major name already exists")

        return new_major

    def update_major(self, user_id, major_id, data):
        """
        Updates a specific major.

        Args:
            user_id: The ID of the user.
            major_id: The ID of the major.
            data: The data to update the major with.

        Returns:
            The updated major.

        Raises:
            ValueError: If there is a validation error, the major is not found,
            or the major name already exists.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Validate data
        try:
            data = major_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        user = storage.get(User, user_id)
        if not user or user.role != "recruiter":
            raise UnauthorizedError("Unauthorized")

        # Get major and update attributes
        major = storage.get(Major, major_id)
        if not major:
            raise ValueError("Major not found")

        for key, value in data.items():
            setattr(major, key, value)
        try:
            storage.save()
        except IntegrityError:
            raise ValueError("Major name already exists")

        return major

    def delete_major(self, user_id, major_id):
        """
        Deletes a specific major.

        Args:
            user_id: The ID of the user.
            major_id: The ID of the major.

        Raises:
            ValueError: If the major is not found.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Check if user is a recruiter
        user = storage.get(User, user_id)
        if not user or user.role != "recruiter":
            raise UnauthorizedError("Unauthorized")

        # Get major
        major = storage.get(Major, major_id)
        if not major:
            raise ValueError("Major not found")

        # Delete major
        storage.delete(major)
        storage.save()
