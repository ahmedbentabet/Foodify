from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from models import storage
from models.order import Order
from models.order_item import OrderItem
from models.menu_item import MenuItem
import uuid

order_routes = Blueprint('order_routes', __name__)

@order_routes.route("/api/v1/orders/update_item", methods=["POST"])
@login_required
def update_order_item():
    """Update or create order item"""
    try:
        data = request.get_json()
        meal_id = data.get('meal_id')
        quantity_change = data.get('quantity_change')

        print(f"DEBUG: Received request - meal_id: {meal_id}, quantity_change: {quantity_change}")
        print(f"DEBUG: Current user ID: {current_user.id}")

        if not meal_id or quantity_change is None:
            return jsonify({"error": "Missing required fields"}), 400

        # Get or create active order for user
        active_order = None
        orders = storage.all(Order).values()
        print(f"DEBUG: Found {len(list(orders))} total orders")
        
        for order in orders:
            if order.client_id == current_user.id and order.status == "active":
                active_order = order
                print(f"DEBUG: Found active order {order.id}")
                break

        if not active_order and quantity_change > 0:
            # Create new order if increasing quantity
            active_order = Order(client_id=current_user.id, status="active")
            storage.new(active_order)
            print(f"DEBUG: Created new order {active_order.id}")
            # Must save here to get the order ID
            storage.save()

        if active_order:
            # Find existing order item
            order_item = None
            if hasattr(active_order, 'order_items'):
                for item in active_order.order_items:
                    if item.menu_item_id == meal_id:
                        order_item = item
                        print(f"DEBUG: Found existing order item {item.id}")
                        break

            if order_item:
                # Update existing order item
                new_quantity = order_item.quantity + quantity_change
                if new_quantity <= 0:
                    storage.delete(order_item)
                else:
                    order_item.quantity = new_quantity
                    print(f"DEBUG: Updated order item quantity to {new_quantity}")
            elif quantity_change > 0:
                # Create new order item
                menu_item = storage.get(MenuItem, meal_id)
                if not menu_item:
                    return jsonify({"error": "Menu item not found"}), 404
                
                order_item = OrderItem(
                    order_id=active_order.id,
                    menu_item_id=meal_id,
                    quantity=quantity_change
                )
                storage.new(order_item)
            storage.save()


            return jsonify({
                "status": "success",
                "order_id": active_order.id,
                "meal_id": meal_id,
                "quantity": order_item.quantity if order_item else 0
            })

        return jsonify({"error": "No active order found"}), 404

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500
