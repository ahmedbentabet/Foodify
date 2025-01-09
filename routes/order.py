from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models import storage
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem
import uuid
from datetime import datetime

order_routes = Blueprint("order_routes", __name__)


@order_routes.route("/api/v1/cart/update", methods=["POST"])
@login_required
def update_cart():
    try:
        data = request.get_json()
        menu_item_id = data.get('menu_item_id')
        action = data.get('action')

        # Validate MenuItem
        menu_item = storage.get(MenuItem, menu_item_id)
        if not menu_item or not menu_item.is_available:
            return jsonify({'error': 'Item not available'}), 400

        # Get active order
        active_order = None
        orders = storage.all(Order).values()
        for order in orders:
            if order.client_id == current_user.id and order.status == 'active':
                active_order = order
                break

        # Create new order if needed
        if not active_order and action == 'increase':
            active_order = Order(
                client_id=current_user.id,
                status='active',
                total_price=0
            )
            storage.new(active_order)
            storage.save()

        # Handle order items
        if active_order:
            # Find existing order item
            order_item = None
            for item in active_order.order_items:
                if item.menu_item_id == menu_item_id:
                    order_item = item
                    break

            if action == 'increase':
                if order_item:
                    order_item.quantity += 1
                else:
                    order_item = OrderItem(
                        order_id=active_order.id,
                        menu_item_id=menu_item_id,
                        quantity=1
                    )
                    storage.new(order_item)
                active_order.total_price = float(active_order.total_price or 0) + float(menu_item.price)

            elif action == 'decrease' and order_item:
                if order_item.quantity > 1:
                    order_item.quantity -= 1
                    active_order.total_price = float(active_order.total_price) - float(menu_item.price)
                else:
                    # Properly remove order item
                    active_order.order_items.remove(order_item)
                    storage.delete(order_item)
                    active_order.total_price = float(active_order.total_price) - float(menu_item.price)

                    # Check if order is empty
                    if not active_order.order_items:
                        active_order.status = 'cancelled'
                        storage.delete(active_order)
                        return jsonify({
                            'success': True,
                            'order': {
                                'total_price': 0,
                                'status': 'cancelled'
                            },
                            'item': {
                                'id': menu_item.id,
                                'quantity': 0
                            }
                        })

            storage.save()

            # Only return response if order still exists
            if active_order.status != 'cancelled':
                return jsonify({
                    'success': True,
                    'order': {
                        'id': active_order.id,
                        'total_price': float(active_order.total_price),
                        'status': active_order.status
                    },
                    'item': {
                        'id': menu_item.id,
                        'quantity': order_item.quantity if order_item else 0
                    }
                })
            else:
                return jsonify({
                    'success': True,
                    'order': None,
                    'item': {
                        'id': menu_item.id,
                        'quantity': 0
                    }
                })

        return jsonify({'error': 'Could not process order'}), 400

    except Exception as e:
        print(f"Error updating cart: {e}")
        return jsonify({'error': str(e)}), 500


@order_routes.route("/api/v1/cart/state", methods=["GET"])
@login_required
def get_cart_state():
    """Get current cart state"""
    try:
        # Get active order
        active_order = None
        orders = storage.all(Order).values()
        for order in orders:
            if order.client_id == current_user.id and order.status == 'active':
                active_order = order
                break

        if active_order:
            return jsonify({
                'items': [{
                    'menu_item_id': item.menu_item_id,
                    'quantity': item.quantity
                } for item in active_order.order_items],
                'order': {
                    'total_price': float(active_order.total_price)
                }
            })

        return jsonify({
            'items': [],
            'order': None
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500
