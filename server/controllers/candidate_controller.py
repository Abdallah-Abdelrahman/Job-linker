"""
This module provides a controller for the Candidate model in the
Job-linker application.
"""

from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

from server.controllers.education_controller import EducationController
from server.controllers.schemas import candidate_schema
from server.controllers.work_experience_controller import WorkExperienceController
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.education import Education
from server.models.job import Job
from server.models.language import Language
from server.models.major import Major
from server.models.recruiter import Recruiter
from server.models.skill import Skill
from server.models.user import User
from server.models.work_experience import WorkExperience


class CandidateController:
    """
    Controller for Candidate model.
    """

    def __init__(self):
        """
        Initializes the CandidateController.
        """
        self.work_experience_controller = WorkExperienceController()
        self.education_controller = EducationController()

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
            # raise ValueError("Candidate already exists for this user")
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
        Gets the current candidate and all related information.

        Args:
            user_id: The ID of the user.

        Returns:
            A dictionary containing the candidate's information,
            work experiences, and educations.

        Raises:
            ValueError: If the candidate is not found.
            UnauthorizedError: If the user role is not 'candidate'.
        """
        # Check user role
        user = storage.get(User, user_id)
        if not user or user.role != "candidate":
            raise UnauthorizedError("User is not authorized")

        # Get candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise ValueError("Candidate not found")

        # Get major
        major = storage.get_by_attr(Major, "id", candidate.major_id)

        # Get work experiences
        work_experiences = storage.get_all_by_attr(
            WorkExperience, "candidate_id", candidate.id
        )

        # Get education entries
        educations = storage.get_all_by_attr(
            Education, "candidate_id", candidate.id)

        # Construct the response
        candidate_data = {
            "id": candidate.id,
            "user_id": candidate.user_id,
            "major": major.to_dict,
            "skills": [skill.to_dict for skill in candidate.skills],
            "languages": [
                language.to_dict for language in candidate.languages
                ],
            "work_experiences": [we.to_dict for we in work_experiences],
            "educations": [edu.to_dict for edu in educations],
        }

        return candidate_data

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
                    {"job": job, "has_applied": has_applied})

        return recommended_jobs

    def add_work_experience(self, user_id, data):
        """
        Adds a work experience to the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            data (dict): The data of the work experience to be added.

        Returns:
            WorkExperience: The created work experience object.
        """
        return self.work_experience_controller.create_work_experience(
                user_id,
                data
                )

    def update_work_experience(self, user_id, work_experience_id, data):
        """
        Updates a work experience in the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            work_experience_id (str): The ID of the work experience to
            be updated.
            data (dict): The data to update the work experience with.

        Returns:
            WorkExperience: The updated work experience object.
        """
        return self.work_experience_controller.update_work_experience(
            user_id, work_experience_id, data
        )

    def delete_work_experience(self, user_id, work_experience_id):
        """
        Deletes a work experience from the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            work_experience_id (str): The ID of the work experience to
            be deleted.

        Raises:
            ValueError: If the work experience is not found.
            UnauthorizedError: If the user is not a candidate.
        """
        self.work_experience_controller.delete_work_experience(
            user_id, work_experience_id
        )

    def add_education(self, user_id, data):
        """
        Adds an education entry to the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            data (dict): The data of the education to be added.

        Returns:
            Education: The created education object.
        """
        # Get candidate ID from user ID
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        return self.education_controller.create_education(
                candidate.id, data
                )

    def update_education(self, user_id, education_id, data):
        """
        Updates an education entry in the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            education_id (str): The ID of the education to be updated.
            data (dict): The data to update the education with.

        Returns:
            Education: The updated education object.
        """
        # Get candidate ID from user ID
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        return self.education_controller.update_education(
            candidate.id, education_id, data
        )

    def delete_education(self, user_id, education_id):
        """
        Deletes an education entry from the candidate's profile.

        Args:
            user_id (str): The ID of the user.
            education_id (str): The ID of the education to be deleted.

        Raises:
            ValueError: If the education entry is not found.
            UnauthorizedError: If the user is not a candidate.
        """
        # Get candidate ID from user ID
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        self.education_controller.delete_education(
                candidate.id,
                education_id
                )
