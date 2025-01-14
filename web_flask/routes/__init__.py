from flask import Blueprint

app_blueprint = Blueprint("app_blueprint", __name__)
from routes.signup import *