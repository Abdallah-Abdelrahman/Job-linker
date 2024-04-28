"""
This module provides a controller for the Recruiter model in the
Job-linker application.
"""

from marshmallow import ValidationError

from server.controllers.schemas import recruiter_schema
from server.models import storage
from server.models.recruiter import Recruiter


class RecruiterController:
    """
    Controller for Recruiter model.
    """

    def __init__(self):
        """
        Initializes the RecruiterController.
        """
        pass

    def create_recruiter(self, user_id, data):
        """
        Creates a new recruiter.

        Args:
            user_id: The ID of the user.
            data: The data of the recruiter to be created.

        Returns:
            The created recruiter.

        Raises:
            ValueError: If there is a validation error.
        """
        # Validate data
        try:
            data = recruiter_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Create new recruiter
        new_recruiter = Recruiter(
            user_id=user_id,
            company_name=data["company_name"],
            company_info=data.get("company_info"),
        )
        storage.new(new_recruiter)
        storage.save()

        return new_recruiter

    def get_current_recruiter(self, user_id):
        """
        Gets the current recruiter.

        Args:
            user_id: The ID of the user.

        Returns:
            The current recruiter.

        Raises:
            ValueError: If the recruiter is not found.
        """
        # Get recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise ValueError("Recruiter not found")

        return recruiter

    def update_current_recruiter(self, user_id, data):
        """
        Updates the current recruiter.

        Args:
            user_id: The ID of the user.
            data: The data to update the recruiter with.

        Returns:
            The updated recruiter.

        Raises:
            ValueError: If there is a validation error or the recruiter
            is not found.
        """
        # Validate data
        try:
            data = recruiter_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Get recruiter and update attributes
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise ValueError("Recruiter not found")

        for key, value in data.items():
            setattr(recruiter, key, value)
        storage.save()

        return recruiter
