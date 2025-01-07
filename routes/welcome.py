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


@welcome_routes.route("/api/v1/search", methods=["GET"], strict_slashes=False)
def search_meals():
    """Search meals endpoint"""
    from models.menu_item import MenuItem
    try:
        query = request.args.get("query", "").strip().lower()
        restaurant = request.args.get("restaurant", "All").strip()
        page = int(request.args.get("page", 1))
        per_page = 8

        # Get all meals with basic filtering
        all_meals = storage.all(MenuItem).values()
        
        # Single-pass filtering with error handling
        filtered_meals = []
        for meal in all_meals:
            try:
                name_matches = query in meal.name.lower()
                # Compare restaurant names exactly as they appear in the select options
                restaurant_matches = (restaurant == "All" or 
                                   meal.restaurant.name.strip() == restaurant.strip())
                
                if name_matches and restaurant_matches:
                    filtered_meals.append(meal)
            except AttributeError:
                # Skip meals with missing attributes
                continue

        # Calculate pagination
        total_meals = len(filtered_meals)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_meals = filtered_meals[start_idx:end_idx]

        return jsonify({
            "meals": [{
                **meal.to_dict(),
                "restaurant_name": meal.restaurant.name.replace(" ", "_"),
                "image_name": meal.name.replace(" ", "_") + ".png"
            } for meal in paginated_meals],
            "total": total_meals,
            "status": "success"
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e),
            "meals": [],
            "total": 0
        }), 500