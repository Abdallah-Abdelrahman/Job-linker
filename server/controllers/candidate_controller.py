"""
This module provides a controller for the Candidate model in the
Job-linker application.
"""

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.controllers.schemas import candidate_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.language import Language
from server.models.major import Major
from server.models.recruiter import Recruiter
from server.models.skill import Skill
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
        # Check if user is a recruiter
        existing_recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if existing_recruiter:
            raise ValueError("A recruiter cannot create a candidate profile")

        # Check if candidate already exists
        existing_candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if existing_candidate:
            #raise ValueError("Candidate already exists for this user")
            return existing_candidate

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

    def add_skill(self, user_id, skill_id):
        """
        Adds a skill to the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            skill_id (str): The ID of the skill to be added.

        Returns:
            Candidate: The updated candidate object.

        Raises:
            ValueError: If the user ID or skill ID is not provided, or if
            the candidate or skill does not exist, or if the skill is
            already added.
            UnauthorizedError: If the user is not a candidate.
        """
        if not user_id or not skill_id:
            raise ValueError("User ID and Skill ID must be provided")

        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        skill = storage.get(Skill, skill_id)
        if not skill:
            raise ValueError("Skill not found")

        if skill in candidate.skills:
            return candidate

        try:
            candidate.skills.append(skill)
            storage.save()
        except IntegrityError:
            storage.rollback()

        return candidate

    def remove_skill(self, user_id, skill_id):
        """
        Removes a skill from the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            skill_id (str): The ID of the skill to be removed.

        Returns:
            Candidate: The updated candidate object.

        Raises:
            ValueError: If the user ID or skill ID is not provided, or
            if the candidate or skill does not exist, or if the skill is
            not already removed.
            UnauthorizedError: If the user is not a candidate.
        """
        if not user_id or not skill_id:
            raise ValueError("User ID and Skill ID must be provided")

        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        skill = storage.get(Skill, skill_id)
        if not skill:
            raise ValueError("Skill not found")

        if skill not in candidate.skills:
            raise ValueError("Skill already removed")

        # Remove skill from candidate
        candidate.skills.remove(skill)
        storage.save()

        return candidate

    def add_language(self, user_id, lang_id):
        """
        Adds a language to the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            lang_id (str): The ID of the language to be added.

        Returns:
            Candidate: The updated candidate object.

        Raises:
            ValueError: If the user ID or language ID is not provided,
            or if the candidate or language does not exist, or if the
            language is already added.
            UnauthorizedError: If the user is not a candidate.
        """
        if not user_id or not lang_id:
            raise ValueError("User ID and Language ID must be provided")

        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        language = storage.get(Language, lang_id)
        if not language:
            raise ValueError("Language not found")

        if language in candidate.languages:
            # raise ValueError("Language already added")
            return candidate

        try:
            candidate.languages.append(language)
            storage.save()
        except IntegrityError:
            storage.rollback()

        return candidate

    def remove_language(self, user_id, lang_id):
        """
        Removes a language from the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            lang_id (str): The ID of the language to be removed.

        Returns:
            Candidate: The updated candidate object.

        Raises:
            ValueError: If the user ID or language ID is not provided,
            or if the candidate or language does not exist, or if the
            language is not already removed.
            UnauthorizedError: If the user is not a candidate.
        """
        if not user_id or not lang_id:
            raise ValueError("User ID and Language ID must be provided")

        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        language = storage.get(Language, lang_id)
        if not language:
            raise ValueError("Language not found")

        if language not in candidate.languages:
            raise ValueError("Language already removed")

        # Remove language from candidate
        candidate.languages.remove(language)
        storage.save()

        return candidate

    def recommend_jobs(self, user_id):
        """
        Recommend jobs for a specific candidate.

        This method returns a list of jobs that are recommended for the
        specified candidate based on their skills and major.

        Args:
            user_id: The ID of the candidate to fetch recommendations for.

        Returns:
            A list of Job objects that are recommended for the candidate.
        """
        # Check user role
        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError()

        # Get candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        # Fetch the candidate's skills and major
        candidate_skills = [skill.name for skill in candidate.skills]
        candidate_major = candidate.major.name

        # Fetch all jobs
        all_jobs = storage.all(Job).values()

        # Filter jobs based on the candidate's skills and major
        recommended_jobs = []
        for job in all_jobs:
            job_skills = [skill.name for skill in job.skills]
            job_major = job.major.name
            # Check if the candidate's skills match the job's skills
            # and the candidate's major matches the job's major
            if (
                set(candidate_skills).intersection(job_skills)
                and candidate_major == job_major
            ):
                # Check if the candidate has applied for this job before
                has_applied = any(
                    application.job_id == job.id
                    for application in candidate.applications
                )
                recommended_jobs.append(
                        {"job": job, "has_applied": has_applied}
                        )

        return recommended_jobs
