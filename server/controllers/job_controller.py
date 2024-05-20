"""
This module provides a controller for the Job model in the
Job-linker application.
"""

import json

from fuzzywuzzy import fuzz
from marshmallow import ValidationError

from server.controllers.schemas import job_schema
from server.email_templates import (
    rejection_email,
    shortlisted_candidates_email,
    shortlisted_email,
)
from server.exception import UnauthorizedError
from server.models import storage
from server.models.application import Application
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.major import Major
from server.models.recruiter import Recruiter
from server.models.skill import Skill
from server.models.user import User
from server.services.mail import MailService


class JobController:
    """
    Controller for Job model.
    """

    MATCH_SCORE_THRESHOLD = 0.4
    STATUS_SHORTLISTED = "shortlisted"
    STATUS_REJECTED = "rejected"

    def __init__(self):
        """
        Initializes the JobController.
        """
        self.email_service = MailService()

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

        # Check if a job with the same details already exists
        existing_job = storage.get_by_attr(Job, "job_title", data["job_title"])
        if existing_job and existing_job.job_description == data[
                "job_description"
                ]:
            raise ValueError(
                    "A job with the same title and description already exists"
                    )

        # Create new job
        new_job = Job(
            recruiter_id=recruiter.id,
            major_id=data["major_id"],
            job_title=data["job_title"],
            job_description=data["job_description"],
            exper_years=data.get("exper_years"),
            salary=data.get("salary"),
            location=data.get("location"),
            responsibilities=data.get("responsibilities", {}),
            application_deadline=data.get("application_deadline"),
            is_open=data.get("is_open", True),
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

        # Get job
        job = storage.get(Job, job_id)
        if not job:
            raise ValueError("Job not found")
        if recruiter and job.recruiter_id != recruiter.id:
            raise ValueError("Job not found")

        # Get applications for the job
        applications = []
        if job:
            applications = storage.get_all_by_attr(
                    Application,
                    "job_id",
                    job.id
                    )

        if recruiter:
            # If the user is a recruiter, provide a list of the applied
            # candidates names and emails
            applied_candidates = [
                {
                    "id": app.candidate.user.id,
                    "name": app.candidate.user.name,
                    "email": app.candidate.user.email,
                    "application_status": app.application_status,
                }
                for app in applications
                if app.candidate and app.candidate.user
            ]
            return {
                "id": job.id,
                "job_title": job.job_title,
                "job_description": job.job_description,
                "location": job.location,
                "salary": job.salary,
                "applied_candidates": applied_candidates,
                "created_at": job.created_at,
                "application_deadline": job.application_deadline,
                "is_open": job.is_open,
                'responsibilities': job.responsibilities
            }

        # If the user is a candidate, add a count displays the number
        # of the candidates who applied for this job
        rec_user = storage.get_by_attr(Recruiter, "id", job.recruiter_id)
        if rec_user:
            company_name = json.loads(
                    rec_user.user.contact_info
                    ).get("company_name")
            return {
                "id": job.id,
                "job_title": job.job_title,
                "created_at": job.created_at,
                "job_description": job.job_description,
                "applications_count": len(applications),
                "company_name": company_name,
                "location": job.location,
                "salary": job.salary,
                "exper_years": job.exper_years,
                "skills": [skill.name for skill in job.skills],
                "application_deadline": job.application_deadline,
                "is_open": job.is_open,
                "responsibilities": job.responsibilities,
            }
        # raise ValueError("Recruiter not found")
        return job.to_dict

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

        # Check if the job is being closed
        is_being_closed = job.is_open and not data.get("is_open", True)

        for key, value in data.items():
            setattr(job, key, value)

        # If the job is closed, shortlist candidates and send emails
        # and notify the recruiter with the shortlisted candidates
        if is_being_closed:
            self.handle_job_closure(job, recruiter)

        storage.save()

        return job

    def handle_job_closure(self, job, recruiter):
        """Handle Job Closing Process and email notifications"""
        applications = storage.get_all_by_attr(Application, "job_id", job.id)
        shortlisted_candidates = []
        for application in applications:
            candidate = storage.get(Candidate, application.candidate_id)
            email = candidate.user.email
            name = candidate.user.name
            contact_info = candidate.user.contact_info
            company_name = json.loads(
                    recruiter.user.contact_info
                    ).get("company_name")
            job_title = job.job_title

            if application.match_score > self.MATCH_SCORE_THRESHOLD:
                application.application_status = self.STATUS_SHORTLISTED
                template = shortlisted_email(name, company_name, job_title)
                shortlisted_candidates.append((name, email, contact_info))
            else:
                application.application_status = self.STATUS_REJECTED
                template = rejection_email(name, company_name, job_title)

            self.email_service.send_mail(template, email, name)
            storage.save()

        recruiter_email = recruiter.user.email
        shortlisted_template = shortlisted_candidates_email(
            recruiter.user.name,
            company_name,
            job_title,
            shortlisted_candidates
        )
        self.email_service.send_mail(
                shortlisted_template,
                recruiter_email, "Recruiter"
                )

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

        # Add skill to job only if it's not already added
        if skill not in job.skills:
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
        Gets all jobs for a user based on their role.

        If the user is a candidate, it returns all jobs for their major.
        If the user is a recruiter, it returns all jobs posted by them.

        Args:
            user_id: The ID of the user.

        Returns:
            The jobs for the user based on their role.

        Raises:
            ValueError: If no jobs are found for the user's role.
            UnauthorizedError: If the user is not a candidate or a recruiter.
        """

        def create_job_data(job, applications, company_name=None):
            """Helper function to create job data dictionary."""
            job_data = {
                "id": job.id,
                "job_title": job.job_title,
                "created_at": job.created_at,
                "job_description": job.job_description,
                "applications_count": len(applications),
                "application_deadline": job.application_deadline,
                "is_open": job.is_open,
                "location": job.location,
                "salary": job.salary,
                "exper_years": job.exper_years,
                "skills": [skill.name for skill in job.skills],
                "responsibilities": job.responsibilities,
            }
            if company_name is not None:
                job_data.update({"company_name": company_name})
            return job_data

        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if candidate:
            jobs = storage.get_all_by_attr(Job, "major_id", candidate.major_id)
            if not jobs:
                raise ValueError("No jobs found for your major")

            return [
                create_job_data(
                    job,
                    storage.get_all_by_attr(Application, "job_id", job.id),
                    json.loads(recruiter.user.contact_info).get("company_name")
                    if recruiter and recruiter.user
                    and recruiter.user.contact_info
                    else None,
                )
                for job in jobs
                if (recruiter := storage.get_by_attr(
                    Recruiter,
                    "id",
                    job.recruiter_id
                    ))
                is not None
            ]

        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if recruiter:
            jobs = storage.get_all_by_attr(Job, "recruiter_id", recruiter.id)
            if not jobs:
                raise ValueError("No jobs found")

            return [
                create_job_data(
                    job,
                    storage.get_all_by_attr(Application, "job_id", job.id),
                )
                for job in jobs
            ]

        raise UnauthorizedError("You are not a candidate or a recruiter")

    def get_all_jobs_sorted_by_major(self):
        """
        Gets all jobs sorted by their major.

        Returns:
            The jobs sorted by their major.
        """

        def create_job_data(job, applications, company_name=None):
            """Helper function to create job data dictionary."""
            job_data = {
                "id": job.id,
                "job_title": job.job_title,
                "created_at": job.created_at,
                "job_description": job.job_description,
                "applications_count": len(applications),
                "application_deadline": job.application_deadline,
                "is_open": job.is_open,
                "location": job.location,
                "salary": job.salary,
                "exper_years": job.exper_years,
                "skills": [skill.name for skill in job.skills],
                "responsibilities": job.responsibilities,
            }
            if company_name is not None:
                job_data.update(
                    {
                        "company_name": company_name,
                    }
                )
            return job_data

        jobs_dict = storage.all(Job)
        jobs = list(jobs_dict.values())
        jobs.sort(key=lambda job: job.major_id)

        return [
            create_job_data(
                job,
                storage.get_all_by_attr(Application, "job_id", job.id),
                json.loads(recruiter.user.contact_info).get("company_name")
                if recruiter and recruiter.user and recruiter.user.contact_info
                else None,
            )
            for job in jobs
            if (recruiter := storage.get_by_attr(
                Recruiter,
                "id",
                job.recruiter_id
                ))
            is not None
        ]

    def get_job_counts(self):
        """
        Gets the count of all jobs and the count of jobs per major.

        Returns:
            A dictionary with the total count of jobs and the
            count of jobs per major.
        """
        # Get all jobs
        jobs_dict = storage.all(Job)

        # Calculate total job count
        total_count = len(jobs_dict)

        # Calculate job count per major
        major_counts = {}
        for job in jobs_dict.values():
            major = storage.get(Major, job.major_id)
            if major.name not in major_counts:
                major_counts[major.name] = 0
            major_counts[major.name] += 1

        return {"total_count": total_count, "major_counts": major_counts}

    def search_jobs(self, location=None, title=None):
        """
        Search for jobs by location and title.

        Args:
            location (str): The location to search for.
            title (str): The title to search for.

        Returns:
            A list of jobs that match the search criteria.
        """
        jobs_dict = storage.all(Job)
        matched_jobs = {}

        for k, v in jobs_dict.items():
            # Calculate match scores for location and title
            location_score = (
                fuzz.token_set_ratio(location.lower(), v.location.lower())
                if location
                else 100
            )
            title_score = (
                fuzz.token_set_ratio(title.lower(), v.job_title.lower())
                if title
                else 100
            )

            # If both scores are above a certain threshold
            # add the job to the results
            if location_score > 70 and title_score > 70:
                matched_jobs[k] = v

        jobs = list(matched_jobs.values())
        jobs.sort(key=lambda job: job.created_at, reverse=True)

        jobs = [job.to_dict for job in jobs]

        return jobs

    def get_all_jobs_sorted_by_date(self):
        """
        Gets all jobs sorted by created_at, the newest first.

        Returns:
            The jobs sorted by created_at.
        """
        jobs_dict = storage.all(Job)

        jobs = list(jobs_dict.values())

        # Sort jobs by created_at
        jobs.sort(key=lambda job: job.created_at, reverse=True)

        jobs = [job.to_dict for job in jobs]

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
