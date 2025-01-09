"""Signup route handler"""
from flask import Blueprint, render_template, url_for, flash, redirect, session, request, jsonify
import math
from models import storage
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
# from app import foodify_app

welcome_routes = Blueprint('welcome_routes', __name__)

@welcome_routes.route("/")
@welcome_routes.route("/welcome")
def welcome():
    return render_template("welcome.html", title="Welcome to Foodify")


@welcome_routes.route("/api/v1/search", methods=["GET"])
def search_meals():
    """Search meals endpoint"""
    from models.menu_item import MenuItem

    query = request.args.get("query", "").strip().lower()
    restaurant = request.args.get("restaurant", "All").strip()
    page = int(request.args.get("page", 1))
    per_page = 8

    # Get meals from database
    meals = storage.all(MenuItem).values()

    # Filter meals with improved restaurant name matching
    filtered_meals = []
    for meal in meals:
        try:
            name_matches = query in meal.name.lower()
            restaurant_matches = (
                restaurant == "All" or
                meal.restaurant.name.replace('&', 'and') == restaurant.replace('&', 'and')  # Updated comparison
            )

            if name_matches and restaurant_matches:
                filtered_meals.append(meal)
        except Exception as e:
            print(f"Error filtering meal: {e}")  # Add debug logging
            continue

    # Add debug logging
    print(f"Restaurant filter: {restaurant}")
    print(f"Total meals: {len(meals)}")
    print(f"Filtered meals: {len(filtered_meals)}")
    print(f"Restaurant names: {[meal.restaurant.name for meal in meals]}")

    # Rest of the code remains the same
    total = len(filtered_meals)
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_meals = filtered_meals[start_idx:end_idx]

    return jsonify({
        "meals": [{
            "id": meal.id,
            "name": meal.name,
            "price": float(meal.price),
            "is_available": meal.is_available,
            "restaurant_name": meal.restaurant.name,
            "image_name": meal.name
        } for meal in paginated_meals],
        "total": total
    })
