"""
This module contains the configuration settings for the Flask application.

It uses the dotenv module to load environment variables from a .env file.
The environment variables are then used to set the configuration variables
for the Flask application.

The ApplicationConfig class defines the following configuration variables:

- SECRET_KEY: The secret key for the Flask application. It's used for
    session signing.
- SQLALCHEMY_TRACK_MODIFICATIONS: Flask-SQLAlchemy will track modifications of
    objects and emit signals. The default is False.
- SQLALCHEMY_ECHO: SQLAlchemy will log all the statements issued to stderr.
- SESSION_TYPE: Specifies the session type set to "redis".
- SESSION_PERMANENT: Whether the session is permanent or not. Here, False.
- SESSION_USE_SIGNER: The cookie sid will be signed and secure.
- SESSION_REDIS: Specifies the Redis server URL.

Classes:
    ApplicationConfig: A class that contains configuration variables
    for the Flask application.
"""
import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class ApplicationConfig:
    SECRET_KEY = os.environ["SECRET_KEY"]

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    # SESSION_TYPE = "redis"
    # SESSION_PERMANENT = False
    # SESSION_USE_SIGNER = True
    # SESSION_REDIS = redis.from_url("redis://127.0.0.1:6379")
    JWT_SECRET_KEY = os.environ["SECRET_KEY"]

    # Set the lifespan of access tokens to 15 minutes
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)

    # Set the lifespan of refresh tokens to 1 day
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    UPLOAD_JOB = f'{os.getcwd()}/server/jobs'
    UPLOAD_CV = f'{os.getcwd()}/server/cv'
    ALLOWED_EXTENSIONS = {'pdf'}
    MAX_CONTENT_LENGTH = 2 * 1000 * 1000
