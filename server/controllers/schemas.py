"""
This module provides schemas for various models in the Job-linker application.
"""

from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    """
    Schema for the login data.
    """

    email = fields.Email(required=True)
    password = fields.Str(required=True)


login_schema = LoginSchema()


class RegistrationSchema(Schema):
    """
    Schema for the registration data.
    """

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(
        required=True, validate=validate.OneOf(["candidate", "recruiter"])
    )


registration_schema = RegistrationSchema()


class UpdateUserSchema(Schema):
    """
    Schema for updating user data.
    """

    name = fields.Str(required=False)
    email = fields.Email(required=False)
    password = fields.Str(required=False)
    role = fields.Str(
        required=False, validate=validate.OneOf(["candidate", "recruiter"])
    )
    contact_info = fields.Str(required=False)
    bio = fields.Str(required=False)
    image_url = fields.Str(required=False)


update_schema = UpdateUserSchema()


class CandidateSchema(Schema):
    """
    Schema for the Candidate model.
    """

    id = fields.Str(required=False)
    major_id = fields.Str(required=True)


candidate_schema = CandidateSchema()


class RecruiterSchema(Schema):
    """
    Schema for the Recruiter model.
    """

    id = fields.Str(required=False)
    company_name = fields.Str(required=True)
    company_info = fields.Str(required=False)


recruiter_schema = RecruiterSchema()


class JobSchema(Schema):
    """
    Schema for the Job model.
    """

    id = fields.Str(required=False)
    recruiter_id = fields.Str(required=False)
    major_id = fields.Str(required=True)
    job_title = fields.Str(required=True)
    job_description = fields.Str(required=True)
    exper_years = fields.Str(required=False)
    salary = fields.Float(required=False)


job_schema = JobSchema()


class MajorSchema(Schema):
    """
    Schema for the Major model.
    """

    id = fields.Str(required=False)
    name = fields.Str(required=True)


major_schema = MajorSchema()


class SkillSchema(Schema):
    """
    Schema for the Skill model.
    """

    id = fields.Str(required=False)
    name = fields.Str(required=True)


skill_schema = SkillSchema()


class LanguageSchema(Schema):
    """
    Schema for the Language model.
    """

    id = fields.Str(required=False)
    name = fields.Str(required=True)


language_schema = LanguageSchema()


class WorkExperienceSchema(Schema):
    """
    Schema for the WorkExperience model.
    """

    id = fields.Str(required=False)
    title = fields.Str(required=True)
    company = fields.Str(required=True)
    location = fields.Str()
    start_date = fields.DateTime()
    end_date = fields.DateTime()
    description = fields.Str()


work_experience_schema = WorkExperienceSchema()


class ApplicationSchema(Schema):
    """
    Schema for the Application model.
    """

    id = fields.Str(required=False)
    job_id = fields.Str(required=False)
    candidate_id = fields.Str(required=False)
    job_title = fields.Str(required=False)
    application_status = fields.Str(
        required=False,
        validate=validate.OneOf(
            ["applied", "shortlisted", "rejected", "hired"]
            ),
        default="applied",
    )


application_schema = ApplicationSchema()
