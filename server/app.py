#!/usr/bin/env python3
"""Entry point for flask app"""
from flask import Flask, flash, redirect, render_template, url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from models.user import User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "thesecretkey"
app.url_map.strict_slashes = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

CORS(app, resources={r"/*": {"origins": "*"}})

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(str(user_id))


class RegisterForm(FlaskForm):
    name = StringField(
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Name"},
    )
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Email"},
    )
    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=30)],
        render_kw={"placeholder": "Password"},
    )
    role = SelectField(
        "Role", choices=[
            ("candidate", "Candidate"),
            ("recruiter", "Recruiter")
            ]
    )
    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_email = db.session.query(User).filter_by(
                email=email.data
                ).first()
        if existing_email:
            raise ValidationError(
                    "The Email is Already Exist, Use Another one"
                    )


class LoginForm(FlaskForm):
    email = StringField(
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Email"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


@app.route("/hello")
def hello():
    """hello route"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login route"""
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(
                user.password,
                form.password.data
                ):
            login_user(user)
            print(f"User authenticated: {current_user.is_authenticated}")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid email or password")
    return render_template("login.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register route"""
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
                form.password.data
                ).decode("utf-8")
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hashed_password,
            role=form.role.data,
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            # Log the user in after successful registration
            login_user(new_user)
            return redirect(url_for("dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"Failed to add user: {e}", category="error")
    return render_template("register.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
