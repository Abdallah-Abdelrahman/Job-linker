"""
This module defines the data validation schemas for user login and registration

The schemas are defined using the Marshmallow library, which provides a simple
way to validate data against certain criteria. The schemas are used to validate
the incoming data for the login and registration endpoints of the
Flask application.

"""
from marshmallow import Schema, fields


# Schema for the login data
class LoginSchema(Schema):
    """
    Defines the data validation schema for user login.

    Fields:
        email (Email): The user's email. This field is required.
        password (Str): The user's password. This field is required.
    """

    email = fields.Email(required=True)
    password = fields.Str(required=True)


login_schema = LoginSchema()


# Schema for the registration data
class RegistrationSchema(Schema):
    """
    Defines the data validation schema for user registration.

    Fields:
        name (Str): The user's name. This field is required.
        email (Email): The user's email. This field is required.
        password (Str): The user's password. This field is required.
        role (Str): The user's role. This field is required and must be either
        "candidate" or "recruiter".
    """

    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(
            required=True,
            validate=lambda r: r in ["candidate", "recruiter"]
            )


registration_schema = RegistrationSchema()


class UpdateUserSchema(Schema):
    """
    Defines the data validation schema for updating a user.

    Fields:
        name (Str): The user's name. This field is optional.
        email (Email): The user's email. This field is optional.
        password (Str): The user's password. This field is optional.
        role (Str): The user's role. This field is optional and must be either
        "candidate" or "recruiter".
        contact_info (Str): The user's contact information. This field is
        optional.
        bio (Str): The user's bio. This field is optional.
        image_url (Str): The URL of the user's image. This field is optional.
    """

    name = fields.Str(required=False)
    email = fields.Email(required=False)
    password = fields.Str(required=False)
    role = fields.Str(
        required=False, validate=lambda r: r in ["candidate", "recruiter"]
    )
    contact_info = fields.Str(required=False)
    bio = fields.Str(required=False)
    image_url = fields.Str(required=False)


update_schema = UpdateUserSchema()


class CandidateSchema(Schema):
    """
    Defines the data validation schema for a candidate.

    Fields:
        major_id (Str): The major's ID. This field is required.
    """

    major_id = fields.Str(required=True)


candidate_schema = CandidateSchema()


class RecruiterSchema(Schema):
    company_name = fields.Str(required=True)
    company_info = fields.Str(required=False)


recruiter_schema = RecruiterSchema()


class JobSchema(Schema):
    recruiter_id = fields.Str(required=True)
    major_id = fields.Str(required=True)
    job_title = fields.Str(required=True)
    job_description = fields.Str(required=True)
    exper_years = fields.Str(required=False)
    salary = fields.Float(required=False)


job_schema = JobSchema()


class MajorSchema(Schema):
    name = fields.Str(required=True)


major_schema = MajorSchema()
