"""
This module provides a controller for the Recruiter model in the
Job-linker application.
"""
import json
from marshmallow import ValidationError

from server.controllers.schemas import recruiter_schema
from server.models import storage
from server.models.candidate import Candidate
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

    def create_recruiter(self, user_id):
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
        # Check if user is a candidate
        existing_candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if existing_candidate:
            raise ValueError("A candidate cannot create a recruiter profile")

        # Check if recruiter already exists
        existing_recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if existing_recruiter:
            raise ValueError("Recruiter already exists for this user")

        # Create new recruiter
        new_recruiter = Recruiter(
            user_id=user_id,
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
        # Get recruiter and update attributes
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise ValueError("Recruiter not found")

        contact_info = json.loads(recruiter.user.contact_info)
        for key, value in data.items():
            contact_info[key] = value

        recruiter.user.contact_info = json.dumps(contact_info)
        storage.save()

        return recruiter
