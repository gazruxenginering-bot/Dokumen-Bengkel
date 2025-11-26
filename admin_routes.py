"""
Admin Routes - Dashboard dan monitoring endpoints
"""

from flask import Blueprint, render_template, request, jsonify, send_file
from functools import wraps
import os
from io import StringIO

from admin_dashboard import admin_dashboard

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Simple auth decorator - ganti dengan proper auth di production
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')  # GANTI INI!

def require_admin(f):
    """Decorator untuk protect admin routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        password = request.args.get('password') or request.form.get('password')
        
        if not password or password != ADMIN_PASSWORD:
            return render_template('admin_login.html'), 401
        
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login page"""
    
    if request.method == 'POST':
        password = request.form.get('password')
        
        if password == ADMIN_PASSWORD:
            # Set simple session cookie
            from flask import redirect
            response = redirect('/admin/dashboard?password=' + password)
            return response
        else:
            return render_template('admin_login.html', error='Invalid password'), 401
    
    return render_template('admin_login.html')


@admin_bp.route('/dashboard')
@require_admin
def dashboard():
    """Admin dashboard - overview"""
    
    stats = admin_dashboard.get_dashboard_stats()
    recent_orders = admin_dashboard.get_recent_orders(limit=10)
    revenue_data = admin_dashboard.get_revenue_by_date(days=30)
    product_sales = admin_dashboard.get_product_sales()
    
    return render_template('admin_dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         revenue_data=revenue_data,
                         product_sales=product_sales)


@admin_bp.route('/users')
@require_admin
def users():
    """User management page"""
    
    users_list = admin_dashboard.get_users(limit=100)
    top_customers = admin_dashboard.get_top_customers(limit=10)
    
    return render_template('admin_users.html',
                         users=users_list,
                         top_customers=top_customers)


@admin_bp.route('/user/<user_email>')
@require_admin
def user_detail(user_email):
    """Detailed user profile"""
    
    user_data = admin_dashboard.get_user_detail(user_email)
    
    return render_template('admin_user_detail.html', data=user_data)


@admin_bp.route('/orders')
@require_admin
def orders():
    """Orders list page"""
    
    recent_orders = admin_dashboard.get_recent_orders(limit=100)
    status_summary = admin_dashboard.get_payment_status_summary()
    
    return render_template('admin_orders.html',
                         orders=recent_orders,
                         status_summary=status_summary)


@admin_bp.route('/reports')
@require_admin
def reports():
    """Reports & analytics page"""
    
    revenue_data = admin_dashboard.get_revenue_by_date(days=90)
    product_sales = admin_dashboard.get_product_sales()
    
    return render_template('admin_reports.html',
                         revenue_data=revenue_data,
                         product_sales=product_sales)


@admin_bp.route('/api/stats')
@require_admin
def api_stats():
    """API endpoint for dashboard stats"""
    
    stats = admin_dashboard.get_dashboard_stats()
    return jsonify(stats)


@admin_bp.route('/api/revenue')
@require_admin
def api_revenue():
    """API endpoint for revenue data"""
    
    days = request.args.get('days', 30, type=int)
    data = admin_dashboard.get_revenue_by_date(days=days)
    
    return jsonify(data)


@admin_bp.route('/api/users')
@require_admin
def api_users():
    """API endpoint for users"""
    
    limit = request.args.get('limit', 50, type=int)
    users = admin_dashboard.get_users(limit=limit)
    
    return jsonify(users)


@admin_bp.route('/export/orders.csv')
@require_admin
def export_orders():
    """Export orders as CSV"""
    
    csv_data = admin_dashboard.export_orders_csv()
    
    return send_file(
        StringIO(csv_data),
        mimetype="text/csv",
        as_attachment=True,
        download_name="orders.csv"
    )


def init_admin_routes(app):
    """Initialize admin routes with Flask app"""
    app.register_blueprint(admin_bp)
    print("✅ Admin routes initialized")
