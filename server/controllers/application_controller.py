from marshmallow import ValidationError

from server.controllers.schemas import application_schema
from server.exception import UnauthorizedError
from server.models import storage
from server.models.application import Application
from server.models.candidate import Candidate
from server.models.job import Job
from server.models.recruiter import Recruiter
from server.models.user import User


class ApplicationsController:
    def __init__(self):
        pass

    def get_application(self, user_id, application_id=None):
        # Get user
        user = storage.get(User, user_id)
        if not user:
            raise UnauthorizedError("Unauthorized")

        if application_id is None:
            # If user is a recruiter, return all applications for their jobs
            if user.role == "recruiter":
                recruiter = storage.get_by_attr(Recruiter, "user_id", user_id)
                applications = [
                    app for job in recruiter.jobs for app in job.applications
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
            if user.role == "candidate" and application.candidate_id != user_id:
                raise UnauthorizedError("Unauthorized")
            elif user.role == "recruiter" and application.job.recruiter_id != user_id:
                raise UnauthorizedError("Unauthorized")

            applications = [application]

        # Prepare the response
        response = []
        for application in applications:
            if user.role == "candidate":
                response.append(
                    {
                        "job_title": application.job.job_title,
                        "application_status": application.application_status,
                        "company_name": application.job.recruiter.company_name,
                    }
                )
            elif user.role == "recruiter":
                response.append(
                    {
                        "job_title": application.job.job_title,
                        "candidate_name": application.candidate.user.name,
                        "candidate_experience": [
                            exp.title for exp in application.candidate.experiences
                        ],
                        "application_status": application.application_status,
                    }
                )
        return response

    def create_application(self, user_id, data):
        # Validate data
        try:
            data = application_schema.load(data)
        except ValidationError as err:
            raise ValueError(err.messages)

        # Check if user is a candidate
        candidate = storage.get_by_attr(Candidate, "user_id", user_id)
        if not candidate:
            raise UnauthorizedError("You are not a candidate")

        # Get the job by title
        job = storage.get_by_attr(Job, "job_title", data.get("job_title"))
        if not job:
            raise ValueError("Job not found")

        # Create new application with default status "applied"
        new_application = Application(
                candidate_id=candidate.id,
                job_id=job.id,
                **data
                )
        storage.new(new_application)
        storage.save()

        return new_application

    def update_application(self, user_id, application_id, data):
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
        # Get user
        user = storage.get(User, user_id)
        if not user:
            raise UnauthorizedError("Unauthorized")

        # Get application
        application = storage.get(Application, application_id)
        if not application:
            raise ValueError("Application not found")

        # Check if user is the candidate who applied or the recruiter for the job
        if user.role == "candidate" and application.candidate_id != user_id:
            raise UnauthorizedError("Unauthorized")
        elif user.role == "recruiter" and application.job.recruiter_id != user_id:
            raise UnauthorizedError("Unauthorized")

        # Delete application
        storage.delete(application)
        storage.save()