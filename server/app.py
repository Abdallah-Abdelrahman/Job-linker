#!/usr/bin/env python3
"""Entry point for flask app"""
from flask import Flask, abort, jsonify, request, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_session import Session
from marshmallow import Schema, ValidationError, fields

from config import ApplicationConfig
from models import storage
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
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = storage.get(User, user_id)
    return jsonify({"id": user.id, "email": user.email})


@app.route("/register", methods=["POST"])
def register_user():
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
    session.pop("user_id")
    return "200"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
