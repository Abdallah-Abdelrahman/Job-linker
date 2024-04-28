"""
This module provides a controller for the WorkExperience model in the
Job-linker application.
"""

from marshmallow import ValidationError

from server.controllers.schemas import work_experience_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.major import Major
from server.models.work_experience import WorkExperience


class WorkExperienceController:
    """
    Controller for WorkExperience model.
    """

    def __init__(self):
        """
        Initializes the WorkExperienceController.
        """
        pass

    def get_work_experiences(self, user_id, major_id=None):
        """
        Fetches all work experiences for a candidate's major or all
        work experiences.

        Args:
            user_id: The ID of the user.
            major_id: The ID of the major (optional).

        Returns:
            A list of work experiences.

        Raises:
            ValueError: If the major or candidate is not found.
            UnauthorizedError: If the user is not a candidate.
        """
        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Work experiences for the candidate's major or all work experiences
        if major_id is not None:
            major = storage.get(Major, major_id)
            if not major:
                raise ValueError("Major not found")

            candidates = major.candidates
            work_experiences = [
                exp for candidate in candidates for exp in candidate.experiences
            ]
        else:
            work_experiences = storage.all(WorkExperience).values()

        return work_experiences

    def create_work_experience(self, user_id, data):
        """
        Creates a new work experience.

        Args:
            user_id: The ID of the user.
            data: The data of the work experience to be created.

        Returns:
            The created work experience.

        Raises:
            ValueError: If there is a validation error.
            UnauthorizedError: If the user is not a candidate.
        """
        # Validate data
        try:
            data = work_experience_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Create new work experience
        new_work_experience = WorkExperience(candidate_id=candidate.id, **data)
        storage.new(new_work_experience)
        storage.save()

        return new_work_experience

    def update_work_experience(self, user_id, work_experience_id, data):
        """
        Updates a specific work experience.

        Args:
            user_id: The ID of the user.
            work_experience_id: The ID of the work experience.
            data: The data to update the work experience with.

        Returns:
            The updated work experience.

        Raises:
            ValueError: If there is a validation error or the work experience
            is not found.
            UnauthorizedError: If the user is not a candidate.
        """
        # Validate data
        try:
            data = work_experience_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Get work experience and update attributes
        work_experience = storage.get(WorkExperience, work_experience_id)
        if not work_experience or work_experience.candidate_id != candidate.id:
            raise ValueError("WorkExperience not found")

        for key, value in data.items():
            setattr(work_experience, key, value)
        storage.save()

        return work_experience

    def delete_work_experience(self, user_id, work_experience_id):
        """
        Deletes a specific work experience.

        Args:
            user_id: The ID of the user.
            work_experience_id: The ID of the work experience.

        Raises:
            ValueError: If the work experience is not found.
            UnauthorizedError: If the user is not a candidate.
        """
        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Get work experience
        work_experience = storage.get(WorkExperience, work_experience_id)
        if not work_experience or work_experience.candidate_id != candidate.id:
            raise ValueError("WorkExperience not found")

        # Delete work experience
        storage.delete(work_experience)
        storage.save()
