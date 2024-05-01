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
from server.models.recruiter import Recruiter


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

        # Create new job
        new_job = Job(
            recruiter_id=recruiter.id,
            major_id=data["major_id"],
            job_title=data["job_title"],
            job_description=data["job_description"],
            exper_years=data.get("exper_years"),
            salary=data.get("salary"),
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
