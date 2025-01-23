#!/usr/bin/env python3
"""
Foodify Web Application

This module serves as the main entry point for the Foodify web application.
It initializes the Flask application, sets up authentication,
registers blueprints, and configures error handlers.
"""
from typing import Optional, Any, Tuple
from flask import Flask, render_template
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import storage
from models.client import Client

# Import route blueprints
from routes.delivery import delivery_routes
from routes.payment import payment_routes
from routes.order import order_routes
from routes.welcome import welcome_routes
from routes.signup import signup_routes
from routes.user_setting import setting_routes
from routes.contact import contact_routes
from routes.login import login_routes, logout_routes
from routes.restaurant import restaurant_routes

# Application initialization
foodify_app: Flask = Flask(__name__, template_folder="templates")
foodify_app.config["SECRET_KEY"] = (
    "0e12c1e7483fe5a5e0088620aa95b29d265213904ca0fb375d558ab9ceaa4991"
)

# Authentication setup
login_manager: LoginManager = LoginManager(foodify_app)
login_manager.login_view = "login_routes.login"
login_manager.login_message_category = "info"
bcrypt: Bcrypt = Bcrypt(foodify_app)


@login_manager.user_loader
def load_user(user_id: str) -> Optional[Client]:
    """
    Load a user from the database by their ID.

    Args:
        user_id: The unique identifier of the user

    Returns:
        Client object if found, None otherwise
    """
    clients = storage.all(Client).values()
    return next((client for client in clients if client.id == user_id), None)


def close_db(error: Optional[Exception] = None) -> None:
    """
    Close database connection after request completion.

    Args:
        error: Optional exception that occurred during request
    """
    storage.close()


# Error handlers
@foodify_app.errorhandler(403)
def forbidden_error(error: Any) -> Tuple[str, int]:
    """
    Handle 403 Forbidden errors.

    Args:
        error: The error that triggered this handler

    Returns:
        Tuple of rendered template and status code
    """
    return render_template('403.html'), 403


@foodify_app.errorhandler(404)
def not_found_error(error: Any) -> Tuple[str, int]:
    """
    Handle 404 Not Found errors.

    Args:
        error: The error that triggered this handler

    Returns:
        Tuple of rendered template and status code
    """
    return render_template('404.html'), 404


@foodify_app.errorhandler(500)
def internal_error(error: Any) -> Tuple[str, int]:
    """
    Handle 500 Internal Server errors.

    Args:
        error: The error that triggered this handler

    Returns:
        Tuple of rendered template and status code
    """
    storage.rollback()  # Rollback database transaction on error
    return render_template('500.html'), 500


# Register blueprints
blueprints = [
    login_routes,
    logout_routes,
    setting_routes,
    signup_routes,
    welcome_routes,
    order_routes,
    payment_routes,
    delivery_routes,
    contact_routes,
    restaurant_routes
]

for blueprint in blueprints:
    foodify_app.register_blueprint(blueprint)

# Register cleanup function
foodify_app.teardown_appcontext(close_db)

if __name__ == "__main__":
    foodify_app.run(debug=True)
