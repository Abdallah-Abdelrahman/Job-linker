"""
This module provides a controller for the Job model in the
Job-linker application.
"""

from marshmallow import ValidationError

from server.controllers.schemas import job_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.major import Major
from server.models.recruiter import Recruiter
from server.models.skill import Skill
from server.models.user import User


class JobController:
    """
    Controller for Job model.
    """

    def __init__(self):
        """
        Initializes the JobController.
        """
        pass

    def create_job(self, user_id, data):
        """
        Creates a new job.

        Args:
            user_id: The ID of the user.
            data: The data of the job to be created.

        Returns:
            The created job.

        Raises:
            ValueError: If there is a validation error or the user is not a
            recruiter.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Validate data
        try:
            data = job_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError("You are not a recruiter")

        # Check if the major exists
        major = storage.get(Major, data["major_id"])
        if not major:
            raise ValueError("Major not found")

        # Create new job
        new_job = Job(
            recruiter_id=recruiter.id,
            major_id=data["major_id"],
            job_title=data["job_title"],
            job_description=data["job_description"],
            exper_years=data.get("exper_years"),
            salary=data.get("salary"),
            location=data.get("location"),
        )
        storage.new(new_job)
        storage.save()

        return new_job

    def get_job(self, user_id, job_id):
        """
        Gets a specific job.

        Args:
            user_id: The ID of the user.
            job_id: The ID of the job.

        Returns:
            The job.

        Raises:
            ValueError: If the job is not found or the user is not a recruiter.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError()

        # Get job
        job = storage.get(Job, job_id)
        if not job or job.recruiter_id != recruiter.id:
            raise ValueError("Job not found")

        return job

    def update_job(self, user_id, job_id, data):
        """
        Updates a specific job.

        Args:
            user_id: The ID of the user.
            job_id: The ID of the job.
            data: The data to update the job with.

        Returns:
            The updated job.

        Raises:
            ValueError: If there is a validation error, the job is not found,
            or the user is not a recruiter.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Validate data
        try:
            data = job_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError()

        # Get job and update attributes
        job = storage.get(Job, job_id)
        if not job or job.recruiter_id != recruiter.id:
            raise ValueError("Job not found")

        for key, value in data.items():
            setattr(job, key, value)
        storage.save()

        return job

    def delete_job(self, user_id, job_id):
        """
        Deletes a specific job.

        Args:
            user_id: The ID of the user.
            job_id: The ID of the job.

        Raises:
            ValueError: If the job is not found or the user is not a recruiter.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError()

        # Get job
        job = storage.get(Job, job_id)
        if not job or job.recruiter_id != recruiter.id:
            raise ValueError("Job not found")

        # Delete job
        storage.delete(job)
        storage.save()

    def add_skill(self, user_id, job_id, skill_id):
        """
        Adds a skill to a job's profile.

        Args:
            user_id (str): The ID of the user (recruiter).
            job_id (str): The ID of the job.
            skill_id (str): The ID of the skill to be added.

        Returns:
            Job: The updated job object.

        Raises:
            ValueError: If the user ID, job ID or skill ID is not provided,
            or if the job or skill does not exist, or if the skill is
            already added.
            UnauthorizedError: If the user is not a recruiter.
        """
        if not user_id or not job_id or not skill_id:
            raise ValueError("User ID, Job ID and Skill ID must be provided")

        user = storage.get(User, user_id)
        if not user or user.role != "recruiter":
            raise UnauthorizedError()

        job = storage.get(Job, job_id)
        if not job:
            raise ValueError("Job not found")

        skill = storage.get(Skill, skill_id)
        if not skill:
            raise ValueError("Skill not found")

        if skill in job.skills:
            raise ValueError("Skill already added")

        # Add skill to job
        job.skills.append(skill)
        storage.save()

        return job

    def remove_skill(self, user_id, job_id, skill_id):
        """
        Removes a skill from a job's profile.

        Args:
            user_id (str): The ID of the user (recruiter).
            job_id (str): The ID of the job.
            skill_id (str): The ID of the skill to be removed.

        Returns:
            Job: The updated job object.

        Raises:
            ValueError: If the user ID, job ID or skill ID is not provided,
            or if the job or skill does not exist, or if the skill is not
            already removed.
            UnauthorizedError: If the user is not a recruiter.
        """
        if not user_id or not job_id or not skill_id:
            raise ValueError("User ID, Job ID and Skill ID must be provided")

        user = storage.get(User, user_id)
        if not user or user.role != "recruiter":
            raise UnauthorizedError()

        job = storage.get(Job, job_id)
        if not job:
            raise ValueError("Job not found")

        skill = storage.get(Skill, skill_id)
        if not skill:
            raise ValueError("Skill not found")

        if skill not in job.skills:
            raise ValueError("Skill already removed")

        # Remove skill from job
        job.skills.remove(skill)
        storage.save()

        return job

    def get_jobs(self, user_id):
        """
        Gets all jobs for a candidate's major.

        Args:
            user_id: The ID of the user.

        Returns:
            The jobs for the candidate's major.

        Raises:
            ValueError: If no jobs are found for the candidate's major or the
            user is not a candidate.
            UnauthorizedError: If the user is not a candidate.
        """
        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Get jobs for the candidate's major
        major_id = candidate.major_id
        jobs = storage.get_all_by_attr(Job, "major_id", major_id)
        if not jobs:
            raise ValueError("No jobs found for your major")

        return jobs

    def get_my_jobs(self, user_id):
        """
        Gets all jobs posted by a recruiter.

        Args:
            user_id: The ID of the user.

        Returns:
            The jobs posted by the recruiter.

        Raises:
            ValueError: If no jobs are found or the user is not a recruiter.
            UnauthorizedError: If the user is not a recruiter.
        """
        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError("You are not a recruiter")

        # Get jobs posted by the recruiter
        jobs = storage.get_all_by_attr(Job, "recruiter_id", recruiter.id)
        if not jobs:
            raise ValueError("No jobs found")

        return jobs

    def recommend_candidates(self, job_id, user_id):
        """
        Recommend candidates for a specific job.

        This method returns a list of candidates that are recommended for
        the specified job based on the job's required skills and major.

        Args:
            job_id: The ID of the job to fetch recommendations for.
            user_id: The ID of the recruiter requesting the recommendations.

        Returns:
            A list of Candidate objects that are recommended for the job.
        """
        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError("You are not a recruiter")

        # Get job
        job = storage.get(Job, job_id)
        if not job:
            raise ValueError("Job not found")

        # Fetch the job's required skills and major
        job_skills = [skill.name for skill in job.skills]
        job_major = job.major.name

        # Fetch all candidates
        all_candidates = storage.all(Candidate).values()

        # Filter candidates based on the job's required skills and major
        recommended_candidates = []
        for candidate in all_candidates:
            candidate_skills = [skill.name for skill in candidate.skills]
            candidate_major = candidate.major.name
            # Check if the job's required skills match the candidate's skills
            # and the job's major matches the candidate's major
            if (
                set(job_skills).intersection(candidate_skills)
                and job_major == candidate_major
            ):
                recommended_candidates.append(candidate)

        return recommended_candidates
