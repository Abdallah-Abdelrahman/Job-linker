"""
This module provides a controller for the WorkExperience model in the
Job-linker application.
"""

from datetime import datetime

from dateutil.parser import parse
from marshmallow import ValidationError

from server.controllers.schemas import work_experience_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.major import Major
from server.models.recruiter import Recruiter
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
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)

        if candidate:
            # Return all work experiences that belong to the candidate
            work_experiences = candidate.experiences
        elif recruiter and major_id is not None:
            # Return all work experiences related to the candidates
            # of a specific major
            major = storage.get(Major, major_id)
            if not major:
                raise ValueError("Major not found")

            candidates = major.candidates
            work_experiences = [
                exp for candidate in candidates
                for exp in candidate.experiences
            ]
        else:
            raise UnauthorizedError()

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

        # Parse dates and convert to ISO format
        for date_field in ["start_date", "end_date"]:
            if date_field in data:
                if isinstance(data[date_field], datetime):
                    data[date_field] = data[date_field].isoformat()
                else:
                    data[date_field] = parse(data[date_field]).isoformat()

        # Check if a work experience with the same details already exists
        existing_work_experience = storage.get_by_attr(
            WorkExperience, "title", data["title"]
        )
        if (
            existing_work_experience
            and existing_work_experience.company == data["company"]
            and existing_work_experience.description == data["description"]
        ):
            return existing_work_experience

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
