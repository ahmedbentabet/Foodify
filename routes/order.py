from flask import Blueprint, jsonify, request, render_template
from flask_login import current_user, login_required
from models import storage
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem
import uuid
from datetime import datetime
from sqlalchemy.exc import PendingRollbackError

order_routes = Blueprint("order_routes", __name__)


@order_routes.route("/api/v1/cart/update", methods=["POST"])
@login_required
def update_cart():
    try:
        data = request.get_json()
        menu_item_id = data.get('menu_item_id')
        action = data.get('action')

        # Ensure clean transaction state
        try:
            storage.rollback()
        except Exception:
            pass

        # Validate MenuItem
        menu_item = storage.get(MenuItem, menu_item_id)
        if not menu_item:
            return jsonify({'error': 'Item not found'}), 404

        # Get/create active order
        active_order = None
        orders = storage.all(Order).values()
        for order in orders:
            if order.client_id == current_user.id and order.status == 'active':
                active_order = order
                break

        if not active_order:
            if action == 'decrease':
                return jsonify({'error': 'No active order found'}), 400
            active_order = Order(
                client_id=current_user.id,
                status='active',
                total_price=0
            )
            storage.new(active_order)
            storage.save()

        # Find order item
        order_item = None
        for item in active_order.order_items:
            if item.menu_item_id == menu_item_id:
                order_item = item
                break

        if action == 'decrease':
            if not order_item:
                return jsonify({'error': 'Item not in cart'}), 400

            # Calculate new price before updating quantity
            new_total = float(active_order.total_price) - \
                float(menu_item.price)

            if order_item.quantity <= 1:
                # Remove item and update order
                active_order.order_items.remove(order_item)
                storage.delete(order_item)
                active_order.total_price = new_total

                # If no items left, cancel order
                if not active_order.order_items:
                    active_order.status = 'cancelled'
                    storage.delete(active_order)
                    storage.save()
                    return jsonify({
                        'success': True,
                        'order': None,
                        'item': {
                            'id': menu_item_id,
                            'quantity': 0
                        }
                    })
            else:
                # Decrease quantity and update price
                order_item.quantity -= 1
                active_order.total_price = new_total

        elif action == 'increase':
            if order_item:
                order_item.quantity += 1
            else:
                order_item = OrderItem(
                    order_id=active_order.id,
                    menu_item_id=menu_item_id,
                    quantity=1
                )
                storage.new(order_item)
            active_order.total_price = float(
                active_order.total_price or 0) + float(menu_item.price)

        storage.save()

        return jsonify({
            'success': True,
            'order': {
                'id': active_order.id,
                'total_price': float(active_order.total_price),
                'status': active_order.status
            },
            'item': {
                'id': menu_item_id,
                'quantity': order_item.quantity if order_item else 0
            }
        })

    except PendingRollbackError:
        storage.rollback()
        return jsonify({'error': 'Transaction error, please try again'}), 500
    except Exception as e:
        storage.rollback()
        print(f"Error updating cart: {e}")
        return jsonify({'error': str(e)}), 500


@order_routes.route("/api/v1/cart/state", methods=["GET"])
@login_required
def get_cart_state():
    """Get current cart state"""
    try:
        # Ensure clean transaction state
        try:
            storage.rollback()
        except Exception:
            pass

        # Get active order
        active_order = None
        menu_items = {}

        orders = storage.all(Order).values()
        for order in orders:
            if order.client_id == current_user.id and order.status == 'active':
                active_order = order
                # Map quantities to menu items
                for item in order.order_items:
                    menu_items[item.menu_item_id] = item.quantity
                break

        return jsonify({
            'items': [{
                'menu_item_id': menu_item_id,
                'quantity': quantity
            } for menu_item_id, quantity in menu_items.items()],
            'order': {
                'id': active_order.id if active_order else None,
                'total_price': float(active_order.total_price) if active_order else 0
            }
        })

    except PendingRollbackError:
        storage.rollback()
        return jsonify({'error': 'Transaction error, please try again'}), 500
    except Exception as e:
        print(f"Error getting cart state: {e}")
        return jsonify({'error': str(e)}), 500


@order_routes.route("/all_orders_and_review")
@login_required
def all_orders_and_review():
    """Display all orders and review page"""
    return render_template("all_orders_and_review.html")
