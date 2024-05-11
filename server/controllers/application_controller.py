"""
This module provides a controller for the Application model in the
Job-linker application.
"""

from datetime import datetime

from marshmallow import ValidationError

from server.controllers.schemas import application_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.application import Application
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.recruiter import Recruiter
from server.models.user import User
from server.services.ai_job_matcher import AIJobMatcher


class ApplicationsController:
    """
    Controller for handling operations related to applications.
    """

    def __init__(self):
        """
        Initialize the ApplicationsController.
        """
        pass

    def get_application(self, user_id, application_id=None):
        """
        Get an application or a list of applications based on the user's role.

        If the user is a recruiter, return all applications for their jobs.
        If the user is a candidate, return all their applications.
        If an application_id is provided, return the specific application.

        Args:
            user_id (str): The ID of the user.
            application_id (str, optional): The ID of the application.
            Defaults to None.

        Raises:
            UnauthorizedError: If the user does not exist or does not have
            the correct role.
            ValueError: If the application does not exist.

        Returns:
            list: A list of dictionaries representing the applications.
        """
        # Get user
        user = storage.get(User, user_id)
        if not user:
            raise UnauthorizedError("Unauthorized")

        if application_id is None:
            # If user is a recruiter, return all applications for their jobs
            if user.role == "recruiter":
                recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
                jobs = storage.get_all_by_attr(
                        Job,
                        "recruiter_id",
                        recruiter.id
                        )
                applications = [
                        app for job in jobs for app in job.applications
                        ]
            # If user is a candidate, return all their applications
            elif user.role == "candidate":
                candidate = storage.get_by_attr(Candidate, "user_id", user_id)
                applications = candidate.applications
            else:
                raise UnauthorizedError("Unauthorized")
        else:
            # Get application
            application = storage.get(Application, application_id)
            if not application:
                raise ValueError("Application not found")

            # Check if user is the candidate who applied or the
            # recruiter for the job
            if (
                user.role == "candidate"
                and application.candidate_id != user.candidate.id
            ):
                raise UnauthorizedError("Unauthorized")
            elif (
                user.role == "recruiter"
                and application.job.recruiter_id != user.recruiter.id
            ):
                raise UnauthorizedError("Unauthorized")

            applications = [application]

        # Prepare the response
        response = []
        for application in applications:
            if user.role == "candidate":
                job_id = application.job.id
                app_job = storage.get(Job, job_id)
                recruiter_id = app_job.to_dict["recruiter_id"]
                recruiter = storage.get(Recruiter, recruiter_id)
                response.append(
                    {
                        "id": application.id,
                        "job_id": application.job.id,
                        "job_title": application.job.job_title,
                        "application_status": application.application_status,
                        "company_name": recruiter.company_name,
                        "salary": application.job.salary,
                        "match_score": application.match_score,
                    }
                )
            elif user.role == "recruiter":
                response.append(
                    {
                        "id": application.id,
                        "job_id": application.job.id,
                        "job_title": application.job.job_title,
                        "candidate_profile": application.candidate.to_dict,
                        "application_status": application.application_status,
                        "match_score": application.match_score,
                    }
                )
        return response

    def create_application(self, user_id, data):
        """
        Create a new application.

        Validate the provided data, check if the user is a candidate,
        get the job by title, and create a new application with default
        status "applied".

        Args:
            user_id (str): The ID of the user.
            data (dict): The data for the new application.

        Raises:
            ValueError: If the data is not valid or the job does not exist.
            UnauthorizedError: If the user is not a candidate.

        Returns:
            Application: The newly created application.
        """
        # Validate data
        try:
            data = application_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Get the job by id
        job = storage.get_by_attr(Job, "id", data.get("job_id"))
        if not job:
            raise ValueError("Job not found")

        # Check if the job is still open for applications
        if not job.is_open:
            raise ValueError("This job is not open for applications")

        # Check if the last date to apply for the job has passed
        if (
                job.application_deadline and
                datetime.utcnow() > job.application_deadline
                ):
            raise ValueError("The last date to apply for this job has passed")

        # Check if the candidate has already applied for this job
        existing_application = storage.get_by_attr(
                Application,
                "job_id",
                job.id
                )
        if (
                existing_application
                and existing_application.candidate_id == candidate.id
                ):
            raise ValueError("You have already applied for this job")

        # Create new application with default status "applied"
        new_application = Application(
            candidate_id=candidate.id,
            job_id=job.id,
        )
        storage.new(new_application)

        matcher = AIJobMatcher(candidate, job)
        match_score = matcher.calculate_match_score()

        new_application.match_score = match_score
        storage.save()

        return new_application

    def update_application(self, user_id, application_id, data):
        """
        Update an existing application.

        Validate the provided data, check if the user is a recruiter,
        get the application by ID, and update the application's attributes.

        Args:
            user_id (str): The ID of the user.
            application_id (str): The ID of the application.
            data (dict): The new data for the application.

        Raises:
            ValueError: If the data is not valid or the application does
            not exist.
            UnauthorizedError: If the user is not a recruiter.

        Returns:
            Application: The updated application.
        """
        # Validate data
        try:
            data = application_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a recruiter
        recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
        if not recruiter:
            raise UnauthorizedError("You are not a recruiter")

        # Get application and update attributes
        application = storage.get(Application, application_id)
        if not application or application.job.recruiter_id != recruiter.id:
            raise ValueError("Application not found")

        for key, value in data.items():
            setattr(application, key, value)
        storage.save()

        return application

    def delete_application(self, user_id, application_id):
        """
        Delete an existing application.

        Get the user and the application by ID, check if the user is the
        candidate who applied
        or the recruiter for the job, and delete the application.

        Args:
            user_id (str): The ID of the user.
            application_id (str): The ID of the application.

        Raises:
            ValueError: If the application does not exist.
            UnauthorizedError: If the user does not exist or does not have the
            correct role.

        Returns:
            None
        """
        # Get user
        user = storage.get(User, user_id)
        if not user:
            raise UnauthorizedError("Unauthorized")

        # Get application
        application = storage.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")

        # Check if user is candidate who applied or the recruiter for the job
        if (
                user.role == "candidate" and
                application.candidate_id != user.candidate.id
                ):
            raise UnauthorizedError("Unauthorized")
        elif (
            user.role == "recruiter"
            and application.job.recruiter_id != user.recruiter.id
        ):
            raise UnauthorizedError("Unauthorized")

        # Delete application
        storage.delete(application)
        storage.save()

    def get_hired_count(self):
        """
        Gets the count of hired candidates.

        Returns:
            The count of hired candidates.
        """
        applications = storage.all(Application)

        hired_count = sum(
            1 for app in applications.values()
            if app.application_status == "hired"
        )

        return hired_count
