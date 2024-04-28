"""
This module provides a controller for the Candidate model in the
Job-linker application.
"""

from marshmallow import ValidationError

from server.controllers.schemas import candidate_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.major import Major
from server.models.user import User


class CandidateController:
    """
    Controller for Candidate model.
    """

    def __init__(self):
        """
        Initializes the CandidateController.
        """
        pass

    def create_candidate(self, user_id, data):
        """
        Creates a new candidate.

        Args:
            user_id: The ID of the user.
            data: The data of the candidate to be created.

        Returns:
            The created candidate.

        Raises:
            ValueError: If there is a validation error or the major
            is not found.
            UnauthorizedError: If the user role is not 'candidate'.
        """
        # Validate data
        try:
            data = candidate_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check user role
        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        # Check if major_id exists
        major_id = data.get("major_id")
        major = storage.get(Major, major_id)
        if not major:
            raise ValueError("Selected Major not found")

        # Create new candidate
        new_candidate = Candidate(
            user_id=user_id,
            major_id=data["major_id"],
        )
        storage.new(new_candidate)
        storage.save()

        return new_candidate

    def get_current_candidate(self, user_id):
        """
        Gets the current candidate.

        Args:
            user_id: The ID of the user.

        Returns:
            The current candidate.

        Raises:
            ValueError: If the candidate is not found.
            UnauthorizedError: If the user role is not 'candidate'.
        """
        # Check user role
        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        # Get candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        return candidate

    def update_current_candidate(self, user_id, data):
        """
        Updates the current candidate.

        Args:
            user_id: The ID of the user.
            data: The data to update the candidate with.

        Returns:
            The updated candidate.

        Raises:
            ValueError: If there is a validation error or the candidate is
            not found.
            UnauthorizedError: If the user role is not 'candidate'.
        """
        # Validate data
        try:
            data = candidate_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check user role
        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        # Get candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        # Update candidate
        for key, value in data.items():
            setattr(candidate, key, value)
        storage.save()

        return candidate

    def delete_current_candidate(self, user_id):
        """
        Deletes the current candidate.

        Args:
            user_id: The ID of the user.

        Raises:
            ValueError: If the candidate is not found.
            UnauthorizedError: If the user role is not 'candidate'.
        """
        # Check user role
        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        # Get candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        # Delete candidate
        storage.delete(candidate)
        storage.save()
