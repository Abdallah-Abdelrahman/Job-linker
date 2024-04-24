#!/usr/bin/env python3
"""
This module serves as the entry point for a Flask application designed for
job recruitment.

The application provides functionalities for user registration, login, and
session management. It serves two types of users: candidates and recruiters.
Candidates can register, login, and manage their sessions. Recruiters can do
the same.

The application uses Flask, SQLAlchemy, Bcrypt, and Flask-Login for
authentication. It also uses Marshmallow for data validation.

Classes:
    LoginSchema: A Schema for validating login data.
    RegistrationSchema: A Schema for validating registration data.

Functions:
    get_current_user(): Returns the current logged-in user's details.
    register_user(): Registers a new user.
    login_user(): Logs in a user.
    logout_user(): Logs out a user.
"""
from flask import Flask, abort, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from marshmallow import Schema, ValidationError, fields

from config import ApplicationConfig
from models import storage
from models.candidate import Candidate
from models.recruiter import Recruiter
from models.user import User

app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.url_map.strict_slashes = False

bcrypt = Bcrypt(app)

CORS(app, supports_credentials=True)
server_session = Session(app)


# Schema for the login data
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


login_schema = LoginSchema()


# Schema for the registration data
class RegistrationSchema(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(
            required=True,
            validate=lambda r: r in ["candidate", "recruiter"]
            )


registration_schema = RegistrationSchema()


@app.route("/@me")
def get_current_user():
    """
        Get the current logged-in user's details.

        Returns:
            A JSON response with the user's id and email if a user is logged in
            Otherwise, it returns a JSON response with an error message and
            a 401 status code.
    """
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = storage.get(User, user_id)
    return jsonify({"id": user.id, "email": user.email})


@app.route("/register", methods=["POST"])
def register_user():
    """
    Register a new user.

    The request data should include name, email, password, and role.
    The role should be either "candidate" or "recruiter".

    Returns:
        A JSON response with the new user's id and email, and 201 status code.
        If a user with the given email already exists, it returns a JSON
        response with an error message and a 409 status code.
    """
    # Validate the request data
    try:
        data = registration_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400

    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data["role"]

    # if a user with the given email already exists
    user = storage.get_user_by_email(email)
    if user:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role
            )
    storage.new(new_user)
    storage.save()

    session["user_id"] = new_user.id

    return jsonify({"id": new_user.id, "email": new_user.email}), 201


@app.route("/login", methods=["POST"])
def login_user():
    """
    Log in a user.

    The request data should include email and password.

    Returns:
        A JSON response with the user's id and email if the login is successful
        If the user does not exist or the password does not match, it returns a
        401 status code.
    """
    # Validate the request data
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        abort(400, description=err.messages)

    email = data["email"]
    password = data["password"]

    user = storage.get_user_by_email(email)

    # If user does not exist or password does not match, return
    if not user or not bcrypt.check_password_hash(user.password, password):
        abort(401, description="Unauthorized")

    session["user_id"] = user.id

    return jsonify({"id": user.id, "email": user.email})


@app.route("/logout", methods=["POST"])
def logout_user():
    """
    Log out a user.

    It removes the user_id from the session.

    Returns:
        A "200" string if the logout is successful.
    """
    session.pop("user_id")
    return "200"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
