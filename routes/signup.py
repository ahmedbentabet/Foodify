#!/usr/bin/env python3
"""Signup route handler"""
from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    redirect,
    session,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    Regexp,
    ValidationError,
)
from models import storage
from flask_login import login_user, current_user


signup_routes = Blueprint("signup_routes", __name__)


class SignUpForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=3, max=70)]
    )
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=3, max=70)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_])[A-Za-z\\d@$!%*?&_]{8,32}$"
            ),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        from models.client import Client

        # Get all clients and check if username exists
        all_clients = storage.all(Client).values()
        for client in all_clients:
            if client.username == username.data:
                raise ValidationError(
                    "Username already exists! Please choose a different one"
                )

    def validate_email(self, email):
        from models.client import Client

        # Get all clients and check if email exists
        all_clients = storage.all(Client).values()
        for client in all_clients:
            if client.email == email.data:
                raise ValidationError(
                    "Email already exists! Please choose a different one"
                )


@signup_routes.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("welcome_routes.welcome"))
    form = SignUpForm()
    if form.validate_on_submit():
        from models.client import Client
        from app import bcrypt

        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode("utf8")
        client = Client(
            username=form.username.data,
            address=form.address.data,
            email=form.email.data,
            password=hashed_password,
        )
        storage.new(client)
        storage.save()
        flash(
            f"Account created successfully for {form.username.data}",
            "success",
        )
        return redirect(url_for("login_routes.login"))
    return render_template("signup.html", title="Sign Up", form=form)
