from flask import Blueprint, render_template, jsonify
from flask_login import current_user, login_required
from models import storage
from models.order import Order

payment_routes = Blueprint("payment_routes", __name__)

@payment_routes.route("/payment")
@login_required
def payment():
    """Display payment page with order details"""
    # Get active order for current user
    active_order = None
    orders = storage.all(Order).values()
    for order in orders:
        if order.client_id == current_user.id and order.status == 'active':
            active_order = order
            break
    
    # Calculate totals
    subtotal = float(active_order.total_price) if active_order else 0.00
    delivery_fee = 5.00
    total = subtotal + delivery_fee
    
    return render_template("payment.html", 
                         subtotal="{:.2f}".format(subtotal),
                         total="{:.2f}".format(total))

@payment_routes.route("/api/v1/payment/totals")
@login_required
def get_totals():
    """Get order totals for AJAX updates"""
    active_order = None
    orders = storage.all(Order).values()
    for order in orders:
        if order.client_id == current_user.id and order.status == 'active':
            active_order = order
            break
    
    subtotal = float(active_order.total_price) if active_order else 0.00
    delivery_fee = 5.00
    total = subtotal + delivery_fee
    
    return jsonify({
        'subtotal': "{:.2f}".format(subtotal),
        'delivery_fee': "{:.2f}".format(delivery_fee),
        'total': "{:.2f}".format(total)
    })
