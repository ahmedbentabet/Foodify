#!/usr/bin/env python3
"""Signup route handler"""
from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    redirect,
    request,
)
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_login import current_user, login_required
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    ValidationError,
    Regexp,
    Optional,
)
from models import storage

setting_routes = Blueprint("setting_routes", __name__)


class UserSettingForm(FlaskForm):
    """User settings form"""

    username = StringField("Username", validators=[DataRequired()])
    address = StringField(
        "Address",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=70,
                message="Address must be between 3 and 70 characters",
            ),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email(message="Please enter a valid email address"),
        ],
    )
    current_password = PasswordField("Current Password")
    new_password = PasswordField(
        "New Password",
        validators=[
            Regexp(
                "^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&_])[A-Za-z\\d@$!%*?&_]{8,32}$",
                message="Password must be 8-32 characters and include uppercase, lowercase, number and special character",
            ),
            Optional(),
        ],
    )
    submit = SubmitField("Submit")

    def validate_email(self, email):
        """Validate email is unique"""
        if email.data != current_user.email:
            from models.client import Client

            clients = storage.all(Client).values()
            if any(client.email == email.data for client in clients):
                raise ValidationError(
                    "Email already exists! Please choose a different one"
                )

    def validate_current_password(self, current_password):
        """Validate current password if new password is provided"""
        if self.new_password.data and not current_password.data:
            raise ValidationError(
                "Current password is required to set new password"
            )


@setting_routes.route("/setting", methods=["GET", "POST"])
@login_required
def setting():
    """Handle user settings"""
    user_setting_form = UserSettingForm()

    if request.method == "GET":
        try:
            from app import bcrypt
            from models.client import Client

            with storage.session_scope() as session:
                client = session.query(Client).get(current_user.id)
                if client:
                    user_setting_form.username.data = client.username
                    user_setting_form.email.data = client.email
                    user_setting_form.address.data = client.address
                return render_template(
                    "user_setting.html", user_setting_form=user_setting_form
                )
        except Exception as e:
            flash(f"Error loading settings: {str(e)}", "danger")
            return redirect(url_for("welcome_routes.welcome"))

    if user_setting_form.validate_on_submit():
        try:
            with storage.session_scope() as session:
                client = session.query(Client).get(current_user.id)
                if not client:
                    flash("User not found", "danger")
                    return redirect(url_for("setting_routes.setting"))

                # Handle password update
                if user_setting_form.new_password.data:
                    if not bcrypt.check_password_hash(
                        client.password,
                        user_setting_form.current_password.data,
                    ):
                        flash("Current password is incorrect", "danger")
                        return redirect(url_for("setting_routes.setting"))

                    client.password = bcrypt.generate_password_hash(
                        user_setting_form.new_password.data
                    ).decode("utf-8")
                    flash("Password updated successfully!", "success")

                # Handle profile updates
                client.email = user_setting_form.email.data
                client.address = user_setting_form.address.data
                flash("Profile information updated successfully!", "success")

        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "danger")

        return redirect(url_for("setting_routes.setting"))

    # If form validation failed, show errors
    for field, errors in user_setting_form.errors.items():
        for error in errors:
            flash(f"{field}: {error}", "danger")

    return redirect(url_for("setting_routes.setting"))
