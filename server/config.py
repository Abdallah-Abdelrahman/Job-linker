"""
This module contains the configuration settings for the Flask application.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class ApplicationConfig:
    """
    A configuration class for the Flask application.

    Attributes:
        SECRET_KEY (str): The secret key for the application. This is used to
            keep client-side sessions secure. from environment variables.

        SQLALCHEMY_TRACK_MODIFICATIONS (bool): `True`, Flask-SQLAlchemy
            will track modifications of objects and emit signals.

        SQLALCHEMY_ECHO (bool): `True`, SQLAlchemy will log all the statements
            issued to stderr which can be useful for debugging.

        JWT_SECRET_KEY (str): The secret key used to sign the JWTs
        (JSON Web Tokens).
            It's fetched from environment variables.

        JWT_ACCESS_TOKEN_EXPIRES (timedelta): The lifespan of access tokens.
            Access tokens expire after 45 minutes.

        JWT_REFRESH_TOKEN_EXPIRES (timedelta): The lifespan of refresh tokens.
            Refresh tokens expire after 1 day.

        UPLOAD_JOB (str): The directory where job-related files will uploaded.

        UPLOAD_CV (str): The directory where CV files will be uploaded.

        ALLOWED_EXTENSIONS (set): The set of file extensions that are allowed
        to be uploaded.
            Currently, only 'pdf' files are allowed.

        MAX_CONTENT_LENGTH (int): The maximum size (in bytes) of the content
        that can be uploaded.
            The current limit is 2 MB.
    """

    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # SESSION_TYPE = "redis"
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    JWT_SECRET_KEY = os.environ["SECRET_KEY"]

    # Set the lifespan of access tokens to 30 minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)

    # Set the lifespan of refresh tokens to 1 day
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    UPLOAD_JOB = f"{os.getcwd()}/server/jobs"
    UPLOAD_CV = f"{os.getcwd()}/server/cv"
    ALLOWED_EXTENSIONS = {"pdf"}
    MAX_CONTENT_LENGTH = 2 * 1000 * 1000
