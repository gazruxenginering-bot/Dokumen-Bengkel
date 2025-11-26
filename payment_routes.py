"""
Payment Routes for DANA Integration
Add these routes to app.py
"""

import uuid
import json
from datetime import datetime
from flask import Blueprint, request, jsonify, render_template

from dana_payment import dana_gateway
from order_manager import order_manager

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')


@payment_bp.route('/docs/premium', methods=['GET', 'POST'])
def premium_docs():
    """
    Premium document access - requires payment
    GET: Display premium doc selection
    POST: Initiate payment
    """
    
    if request.method == 'GET':
        # Display available premium documents/services
        premium_items = [
            {
                "id": "doc_premium_1",
                "name": "Premium Document Bundle 1",
                "description": "Access to exclusive technical documents",
                "price": 50000,  # IDR
                "type": "document_bundle"
            },
            {
                "id": "doc_premium_2",
                "name": "Premium Document Bundle 2",
                "description": "Advanced technical manuals and guides",
                "price": 100000,
                "type": "document_bundle"
            },
            {
                "id": "monthly_subscription",
                "name": "Monthly Subscription",
                "description": "Unlimited access for 30 days",
                "price": 75000,
                "type": "subscription"
            }
        ]
        
        return render_template('premium.html', items=premium_items)
    
    else:  # POST - Create payment order
        data = request.get_json()
        product_id = data.get('product_id')
        user_email = data.get('email')
        
        # Validate input
        if not product_id or not user_email:
            return jsonify({"error": "Missing product_id or email"}), 400
        
        # Create order
        order_id = f"order_{uuid.uuid4().hex[:12]}"
        
        # Determine price based on product
        prices = {
            "doc_premium_1": 50000,
            "doc_premium_2": 100000,
            "monthly_subscription": 75000
        }
        
        amount = prices.get(product_id, 50000)
        
        # Save order to database
        order_result = order_manager.create_order(
            order_id=order_id,
            user_id=user_email,  # Use email as user ID
            user_email=user_email,
            product_id=product_id,
            product_name=f"Premium Access - {product_id}",
            amount=amount,
            product_type="premium_document"
        )
        
        if not order_result['success']:
            return jsonify({"error": "Failed to create order"}), 500
        
        # Create payment with DANA
        payment_result = dana_gateway.create_payment_order(
            order_id=order_id,
            amount=amount / 100,  # Convert to standard currency
            title=f"Premium Document Access",
            description=f"Access to premium documents - {product_id}",
            notify_url=f"{request.host_url.rstrip('/')}/payment/webhook/dana",
            return_url=f"{request.host_url.rstrip('/')}/payment/success/{order_id}"
        )
        
        if not payment_result.get('success'):
            return jsonify({"error": "Failed to create payment"}), 500
        
        # Update order with DANA order ID
        order_manager.update_order_status(
            order_id,
            "PENDING",
            payment_result.get('dana_order_id')
        )
        
        return jsonify({
            "success": True,
            "order_id": order_id,
            "payment_url": payment_result.get('payment_url')
        })


@payment_bp.route('/success/<order_id>', methods=['GET'])
def payment_success(order_id):
    """Handle successful payment redirect from DANA"""
    
    order = order_manager.get_order(order_id)
    
    if not order:
        return render_template('payment_error.html', 
                             error="Order not found", 
                             order_id=order_id), 404
    
    # Verify payment with DANA
    verify_result = dana_gateway.verify_payment(
        order_id=order_id,
        dana_transaction_id=order.get('dana_order_id')
    )
    
    if verify_result.get('verified'):
        # Update order status
        order_manager.update_order_status(order_id, "COMPLETED")
        
        return render_template('payment_success.html',
                             order=order,
                             message="Payment successful! Access granted.")
    else:
        return render_template('payment_pending.html',
                             order=order,
                             message="Payment is being processed. Please wait...")


@payment_bp.route('/webhook/dana', methods=['POST'])
def dana_webhook():
    """
    Webhook handler for DANA payment notifications
    Receives payment status updates from DANA
    """
    
    try:
        webhook_id = str(uuid.uuid4())
        payload = request.get_data(as_text=True)
        data = request.get_json()
        
        order_id = data.get('orderId') or data.get('order_id')
        event_type = data.get('event') or data.get('eventType')
        status = data.get('status')
        
        # Log webhook
        order_manager.log_webhook(webhook_id, order_id, event_type, payload)
        
        if order_id:
            order = order_manager.get_order(order_id)
            
            if order:
                # Update order based on status
                if status == "COMPLETED" or status == "SETTLED":
                    order_manager.update_order_status(order_id, "COMPLETED")
                elif status == "FAILED" or status == "EXPIRED":
                    order_manager.update_order_status(order_id, "FAILED")
                elif status == "PENDING":
                    order_manager.update_order_status(order_id, "PENDING")
                
                return jsonify({"success": True, "webhook_id": webhook_id}), 200
        
        return jsonify({"success": True, "webhook_id": webhook_id}), 200
    
    except Exception as e:
        print(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 400


@payment_bp.route('/status/<order_id>', methods=['GET'])
def payment_status(order_id):
    """Get payment status for an order"""
    
    order = order_manager.get_order(order_id)
    
    if not order:
        return jsonify({"error": "Order not found"}), 404
    
    return jsonify({
        "order_id": order_id,
        "status": order.get('status'),
        "amount": order.get('amount'),
        "created_at": order.get('created_at'),
        "completed_at": order.get('completed_at')
    })


@payment_bp.route('/orders', methods=['GET'])
def get_user_orders():
    """Get user's orders (requires user identification)"""
    
    user_email = request.args.get('email')
    
    if not user_email:
        return jsonify({"error": "Email required"}), 400
    
    orders = order_manager.get_user_orders(user_email)
    
    return jsonify({
        "user": user_email,
        "orders": orders,
        "total": len(orders)
    })


@payment_bp.route('/analytics', methods=['GET'])
def payment_analytics():
    """
    Analytics dashboard for payments
    (Add authentication/authorization here)
    """
    
    import sqlite3
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Total revenue
    cursor.execute("SELECT SUM(amount) as total FROM orders WHERE status = 'COMPLETED'")
    total_revenue = cursor.fetchone()[0] or 0
    
    # Total orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    
    # Completed orders
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'COMPLETED'")
    completed_orders = cursor.fetchone()[0]
    
    # Pending orders
    cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'PENDING'")
    pending_orders = cursor.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "completed_orders": completed_orders,
        "pending_orders": pending_orders,
        "conversion_rate": (completed_orders / total_orders * 100) if total_orders > 0 else 0
    })


def init_payment_routes(app):
    """Initialize payment routes with Flask app"""
    app.register_blueprint(payment_bp)
    print("✅ Payment routes initialized")
