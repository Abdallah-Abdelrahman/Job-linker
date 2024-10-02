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
    os.environ['ANTIWORD_PATH'] = '/usr/bin/antiword'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # SESSION_TYPE = "redis"
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    JWT_SECRET_KEY = os.environ["SECRET_KEY"]
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/refresh'
    JWT_COOKIE_SECURE = True  # Ensure this is True for production (HTTPS)
    JWT_COOKIE_CSRF_PROTECT = False  # Adjust based on your CSRF protection needs

    # Redis configuration
    REDIS_HOST = os.environ["REDIS_HOST"]
    REDIS_PORT = os.environ["REDIS_PORT"]
    REDIS_DB_JWT = os.environ["REDIS_DB_JWT"]
    REDIS_DB_LIMITER = os.environ["REDIS_DB_LIMITER"]

    # Set the lifespan of access tokens to 30 minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Here you can globally configure all the ways you want to allow JWTs to
    # be sent to your web application. By default, this will be only headers.
    JWT_TOKEN_LOCATION = ["headers", "cookies", "json", "query_string"]

    # Set the lifespan of refresh tokens to 1 day
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)

    BASE_UPLOAD_PATH = os.path.join(os.getcwd(), "server")
    UPLOAD_JOB = os.path.join(BASE_UPLOAD_PATH, "jobs")
    UPLOAD_CV = os.path.join(BASE_UPLOAD_PATH, "cvs")
    UPLOAD_IMAGE = os.path.join(BASE_UPLOAD_PATH, "images")
    UPLOAD_TEMP = os.path.join(BASE_UPLOAD_PATH, "temp")
    ALLOWED_EXTENSIONS = {"pdf", "doc", "docx"}
    ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}
    MAX_IMAGE_CONTENT_LENGTH = 2 * 1024 * 1024
    MAX_CONTENT_LENGTH = 2 * 1000 * 1000

    UPLOADED_IMAGE_DEST = "server/images"
    UPLOADED_CV_DEST = "server/cvs"
    UPLOADED_JOB_DEST = "server/jobs"

    for path in [UPLOAD_JOB, UPLOAD_CV, UPLOAD_IMAGE, UPLOAD_TEMP]:
        os.makedirs(path, exist_ok=True)

    # Configure Caching
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300
