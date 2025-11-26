"""
Admin Dashboard Module
For monitoring users, payments, and analytics
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class AdminDashboard:
    """Admin dashboard untuk monitoring payment dan users"""
    
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
    
    def get_dashboard_stats(self) -> Dict:
        """Get overall dashboard statistics"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total revenue
        cursor.execute("SELECT SUM(amount) FROM orders WHERE status = 'COMPLETED'")
        total_revenue = cursor.fetchone()[0] or 0
        
        # Today's revenue
        cursor.execute("""
        SELECT SUM(amount) FROM orders 
        WHERE status = 'COMPLETED' 
        AND DATE(created_at) = DATE('now')
        """)
        today_revenue = cursor.fetchone()[0] or 0
        
        # Total users
        cursor.execute("SELECT COUNT(DISTINCT user_email) FROM orders WHERE user_email IS NOT NULL")
        total_users = cursor.fetchone()[0]
        
        # Total orders
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]
        
        # Completed orders
        cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'COMPLETED'")
        completed_orders = cursor.fetchone()[0]
        
        # Pending orders
        cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'PENDING'")
        pending_orders = cursor.fetchone()[0]
        
        # Failed orders
        cursor.execute("SELECT COUNT(*) FROM orders WHERE status = 'FAILED'")
        failed_orders = cursor.fetchone()[0]
        
        # Conversion rate
        conversion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
        
        # Average order value
        cursor.execute("SELECT AVG(amount) FROM orders WHERE status = 'COMPLETED'")
        avg_order_value = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_revenue": total_revenue,
            "today_revenue": today_revenue,
            "total_users": total_users,
            "total_orders": total_orders,
            "completed_orders": completed_orders,
            "pending_orders": pending_orders,
            "failed_orders": failed_orders,
            "conversion_rate": round(conversion_rate, 2),
            "avg_order_value": round(avg_order_value, 2)
        }
    
    def get_recent_orders(self, limit: int = 20) -> List[Dict]:
        """Get recent orders"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, user_email, product_name, amount, status, created_at 
        FROM orders 
        ORDER BY created_at DESC 
        LIMIT ?
        """, (limit,))
        
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return orders
    
    def get_users(self, limit: int = 50) -> List[Dict]:
        """Get all users with their purchase history"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            user_email,
            COUNT(*) as purchase_count,
            SUM(CASE WHEN status = 'COMPLETED' THEN amount ELSE 0 END) as total_spent,
            MAX(created_at) as last_purchase,
            GROUP_CONCAT(DISTINCT status) as statuses
        FROM orders 
        WHERE user_email IS NOT NULL
        GROUP BY user_email
        ORDER BY total_spent DESC
        LIMIT ?
        """, (limit,))
        
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return users
    
    def get_user_detail(self, user_email: str) -> Dict:
        """Get detailed user profile"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # User summary
        cursor.execute("""
        SELECT 
            user_email,
            COUNT(*) as total_orders,
            COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_orders,
            SUM(CASE WHEN status = 'COMPLETED' THEN amount ELSE 0 END) as total_spent,
            MIN(created_at) as first_purchase,
            MAX(created_at) as last_purchase
        FROM orders 
        WHERE user_email = ?
        """, (user_email,))
        
        user_summary = dict(cursor.fetchone() or {})
        
        # User's orders
        cursor.execute("""
        SELECT id, product_name, amount, status, created_at 
        FROM orders 
        WHERE user_email = ?
        ORDER BY created_at DESC
        """, (user_email,))
        
        orders = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return {
            "user": user_summary,
            "orders": orders
        }
    
    def get_revenue_by_date(self, days: int = 30) -> List[Dict]:
        """Get revenue trend over time"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as orders,
            COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed,
            SUM(CASE WHEN status = 'COMPLETED' THEN amount ELSE 0 END) as revenue
        FROM orders 
        WHERE created_at >= datetime('now', '-' || ? || ' days')
        GROUP BY DATE(created_at)
        ORDER BY date DESC
        """, (days,))
        
        data = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return data
    
    def get_product_sales(self) -> List[Dict]:
        """Get sales by product"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            product_id,
            product_name,
            product_type,
            COUNT(*) as total_orders,
            COUNT(CASE WHEN status = 'COMPLETED' THEN 1 END) as completed_orders,
            SUM(CASE WHEN status = 'COMPLETED' THEN amount ELSE 0 END) as total_revenue,
            AVG(CASE WHEN status = 'COMPLETED' THEN amount END) as avg_price
        FROM orders 
        GROUP BY product_id
        ORDER BY total_revenue DESC
        """)
        
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return products
    
    def get_payment_status_summary(self) -> Dict:
        """Get payment status distribution"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT status, COUNT(*) as count, SUM(amount) as amount
        FROM orders 
        GROUP BY status
        """)
        
        statuses = {}
        for status, count, amount in cursor.fetchall():
            statuses[status] = {
                "count": count,
                "amount": amount or 0
            }
        
        conn.close()
        
        return statuses
    
    def get_top_customers(self, limit: int = 10) -> List[Dict]:
        """Get top spending customers"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            user_email,
            COUNT(*) as orders,
            SUM(CASE WHEN status = 'COMPLETED' THEN amount ELSE 0 END) as total_spent,
            MAX(created_at) as last_order
        FROM orders 
        WHERE user_email IS NOT NULL AND status = 'COMPLETED'
        GROUP BY user_email
        ORDER BY total_spent DESC
        LIMIT ?
        """, (limit,))
        
        customers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return customers
    
    def export_orders_csv(self) -> str:
        """Export all orders as CSV format"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT id, user_email, product_name, amount, status, created_at, completed_at
        FROM orders 
        ORDER BY created_at DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        # Build CSV
        csv_data = "Order ID,Email,Product,Amount,Status,Created,Completed\n"
        for row in rows:
            csv_data += f"{row['id']},{row['user_email']},{row['product_name']},{row['amount']},{row['status']},{row['created_at']},{row['completed_at']}\n"
        
        return csv_data


admin_dashboard = AdminDashboard()
