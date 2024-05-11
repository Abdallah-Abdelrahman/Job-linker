"""
This module provides schemas for various models in the Job-linker application.
"""

from datetime import datetime

from dateutil.parser import parse
from marshmallow import Schema, fields, validate
from marshmallow.fields import DateTime


class MultiFormatDateTime(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        if isinstance(value, datetime):
            return value

        formats = ["%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
        for fmt in formats:
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                pass
        self.fail("invalid")


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
    is_admin = fields.Bool(required=False)


registration_schema = RegistrationSchema()


class UpdateUserSchema(Schema):
    """
    Schema for updating user data.
    """

    name = fields.Str(required=False)
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
    major_id = fields.Str(required=False)
    job_title = fields.Str(required=False)
    location = fields.Str(required=False)
    job_description = fields.Str(required=False)
    exper_years = fields.Str(required=False)
    salary = fields.Float(required=False)
    application_deadline = MultiFormatDateTime()
    is_open = fields.Boolean(required=False)


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
    match_score = fields.Float(required=False)


application_schema = ApplicationSchema()
