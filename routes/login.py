#!/usr/bin/env python3
"""
Login route handler.
"""

from flask import (
    Blueprint,
    render_template,
    url_for,
    flash,
    redirect,
    request,
    jsonify,
    Response,
)
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email
from flask_login import login_user, current_user, logout_user, login_required
from models import storage
from typing import Union, Dict, Any

login_routes = Blueprint("login_routes", __name__)
logout_routes = Blueprint("logout_routes", __name__)
setting_routes = Blueprint("setting_routes", __name__)
order_routes = Blueprint("order_routes", __name__)


class LoginForm(FlaskForm):
    """Form for user login."""

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


@login_routes.route("/login", methods=["GET", "POST"])
def login() -> Union[str, "Response"]:
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for("welcome_routes.welcome"))

    form = LoginForm()
    if form.validate_on_submit():
        try:
            from app import bcrypt
            from models.client import Client

            with storage.session_scope() as session:
                client = (
                    session.query(Client)
                    .filter_by(email=form.email.data)
                    .first()
                )

                if client and bcrypt.check_password_hash(
                    client.password, form.password.data
                ):
                    login_user(client, remember=form.remember.data)
                    next_page = request.args.get("next")
                    return (
                        redirect(next_page)
                        if next_page
                        else redirect(url_for("welcome_routes.welcome"))
                    )
                else:
                    flash(
                        "Login Unsuccessful. Please check credentials",
                        "danger",
                    )

        except Exception as e:
            print(f"Login error: {e}")
            flash("An error occurred during login", "danger")

    return render_template("login.html", title="Login", form=form)


@logout_routes.route("/logout", methods=["GET", "POST"])
def logout() -> "Response":
    """Handle user logout."""
    logout_user()
    return redirect(url_for("welcome_routes.welcome"))


@order_routes.route("/api/v1/orders/add_item", methods=["POST"])
@login_required
def add_menu_item() -> Union[Dict[str, Any], "Response"]:
    """Add or update item in cart."""
    from models.menu_item import MenuItem
    from models.order import Order
    from models.order_item import OrderItem

    try:
        data = request.get_json()
        menu_item_id = data.get("menu_item_id")
        quantity_change = data.get("quantity_change", 1)

        menu_item = storage.get(MenuItem, menu_item_id)
        if not menu_item or not menu_item.is_available:
            return jsonify({"error": "Item not available"}), 400

        active_order = None
        orders = storage.all(Order).values()
        for order in orders:
            if (
                order.client_id == current_user.id
                and order.status == "active"
            ):
                active_order = order
                break

        if not active_order:
            active_order = Order(client_id=current_user.id, status="active")
            storage.new(active_order)
            storage.save()

        order_item = None
        if hasattr(active_order, "order_items"):
            for item in active_order.order_items:
                if item.menu_item_id == menu_item_id:
                    order_item = item
                    break

        if order_item:
            order_item.quantity += quantity_change
            if order_item.quantity <= 0:
                storage.delete(order_item)
        else:
            order_item = OrderItem(
                order_id=active_order.id,
                menu_item_id=menu_item_id,
                quantity=quantity_change,
            )
            storage.new(order_item)

        storage.save()

        return jsonify(
            {
                "status": "success",
                "order_id": active_order.id,
                "item": {
                    "id": menu_item.id,
                    "name": menu_item.name,
                    "price": float(menu_item.price),
                    "quantity": order_item.quantity if order_item else 0,
                },
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
