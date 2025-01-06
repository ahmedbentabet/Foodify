#!/usr/bin/env python3
"""Login route handler"""
from flask import Blueprint, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_login import login_user, current_user, logout_user
from models import storage


login_routes = Blueprint('login_routes', __name__)

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


@login_routes.route("/login", methods=["GET", "POST"])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for("welcome_routes.welcome"))
    form = LoginForm()
    if form.validate_on_submit():
        from models.client import Client
        from app import bcrypt
        # Get all clients and find the one with matching email
        clients = storage.all(Client).values()
        client = None
        for c in clients:
            if c.email == form.email.data:
                client = c
                break
                
        if client and bcrypt.check_password_hash(client.password, form.password.data):
            login_user(client, remember=form.remember.data)
            flash("You have been logged in!", "success")
            return redirect(url_for("welcome_routes.welcome"))
        else:
            flash("Login Unsuccessful. Please check credentials", "danger")
    return render_template("login.html", title="Login", form=form)


@login_routes.route("/login", methods=["GET", "POST"])
def logout():
    logout_user()
    return redirect(url_for("welcome_routes.welcome"))
