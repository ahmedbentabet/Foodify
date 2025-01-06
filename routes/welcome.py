"""Signup route handler"""
from flask import Blueprint, render_template, url_for, flash, redirect, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
# from app import foodify_app

welcome_routes = Blueprint('welcome_routes', __name__)

@welcome_routes.route("/")
@welcome_routes.route("/welcome")
def welcome():
    return render_template("welcome.html", title="Welcome to Foodify")