"""Education Controller"""

from marshmallow import ValidationError

from server.controllers.schemas import education_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.education import Education


class EducationController:
    """
    Controller for Education model.
    """

    def __init__(self):
        """
        Initializes the EducationController.
        """
        pass

    def get_educations(self, candidate_id):
        """
        Fetches all educations for a candidate.

        Args:
            candidate_id: The ID of the candidate.

        Returns:
            A list of educations for the candidate.
        """
        candidate = storage.get(Candidate, candidate_id)
        if not candidate:
            raise UnauthorizedError("Unauthorized")

        return candidate.educations

    def create_education(self, candidate_id, data):
        """
        Creates a new education for a candidate.

        Args:
            candidate_id: The ID of the candidate.
            data: The data of the education to be created.

        Returns:
            The created education.
        """
        # Validate data
        try:
            data = education_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if candidate exists
        candidate = storage.get(Candidate, candidate_id)
        if not candidate:
            raise UnauthorizedError("Unauthorized")

        # Create new education
        new_education = Education(candidate_id=candidate.id, **data)
        storage.new(new_education)
        storage.save()

        return new_education

    def update_education(self, candidate_id, education_id, data):
        """
        Updates a specific education for a candidate.

        Args:
            candidate_id: The ID of the candidate.
            education_id: The ID of the education.
            data: The data to update the education with.

        Returns:
            The updated education.
        """
        # Validate data
        try:
            data = education_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if candidate exists
        candidate = storage.get(Candidate, candidate_id)
        if not candidate:
            raise UnauthorizedError("Unauthorized")

        # Get education and update attributes
        education = storage.get(Education, education_id)
        if not education or education.candidate_id != candidate.id:
            raise ValueError("Education not found")

        for key, value in data.items():
            setattr(education, key, value)
        storage.save()

        return education

    def delete_education(self, candidate_id, education_id):
        """
        Deletes a specific education for a candidate.

        Args:
            candidate_id: The ID of the candidate.
            education_id: The ID of the education.

        Raises:
            ValueError: If the education is not found.
            UnauthorizedError: If the user is not a candidate.
        """
        # Check if candidate exists
        candidate = storage.get(Candidate, candidate_id)
        if not candidate:
            raise UnauthorizedError("Unauthorized")

        # Get education
        education = storage.get(Education, education_id)
        if not education or education.candidate_id != candidate.id:
            raise ValueError("Education not found")

        # Delete education
        storage.delete(education)
        storage.save()
