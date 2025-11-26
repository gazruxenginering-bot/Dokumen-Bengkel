"""
Order Management Database Schema
For DANA Payment tracking and monetization
"""

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict


def init_payment_db(db_path: str = "database.db"):
    """Initialize payment tables in existing database"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Orders table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        user_email TEXT,
        product_id TEXT NOT NULL,
        product_name TEXT NOT NULL,
        product_type TEXT,
        amount REAL NOT NULL,
        currency TEXT DEFAULT 'IDR',
        status TEXT DEFAULT 'PENDING',
        dana_order_id TEXT UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        notes TEXT
    )
    """)
    
    # Transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id TEXT PRIMARY KEY,
        order_id TEXT NOT NULL,
        dana_transaction_id TEXT UNIQUE,
        transaction_type TEXT,
        status TEXT DEFAULT 'PENDING',
        amount REAL NOT NULL,
        fee REAL DEFAULT 0,
        net_amount REAL,
        payment_method TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completed_at TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)
    
    # Payment webhooks log table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_webhooks (
        id TEXT PRIMARY KEY,
        order_id TEXT,
        event_type TEXT,
        payload TEXT,
        status TEXT DEFAULT 'RECEIVED',
        processed_at TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (order_id) REFERENCES orders(id)
    )
    """)
    
    # Pricing/Products table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        description TEXT,
        price REAL NOT NULL,
        currency TEXT DEFAULT 'IDR',
        enabled BOOLEAN DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Payment database tables initialized")


class OrderManager:
    """Manage orders and payment records"""
    
    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
    
    def create_order(self, 
                    order_id: str,
                    user_id: str,
                    product_id: str,
                    product_name: str,
                    amount: float,
                    user_email: str = None,
                    product_type: str = None,
                    notes: str = None) -> Dict:
        """Create new order"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO orders 
            (id, user_id, user_email, product_id, product_name, product_type, amount, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (order_id, user_id, user_email, product_id, product_name, product_type, amount, notes))
            
            conn.commit()
            return {"success": True, "order_id": order_id}
        except Exception as e:
            print(f"Error creating order: {e}")
            return {"success": False, "error": str(e)}
        finally:
            conn.close()
    
    def get_order(self, order_id: str) -> Optional[Dict]:
        """Get order details"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        order = cursor.fetchone()
        conn.close()
        
        return dict(order) if order else None
    
    def update_order_status(self, order_id: str, status: str, dana_order_id: str = None) -> bool:
        """Update order status"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            if dana_order_id:
                cursor.execute("""
                UPDATE orders 
                SET status = ?, dana_order_id = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (status, dana_order_id, order_id))
            else:
                cursor.execute("""
                UPDATE orders 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """, (status, order_id))
            
            if status == "COMPLETED":
                cursor.execute("""
                UPDATE orders SET completed_at = CURRENT_TIMESTAMP WHERE id = ?
                """, (order_id,))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating order: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_orders(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user's orders"""
        
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT * FROM orders 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
        """, (user_id, limit))
        
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return orders
    
    def log_webhook(self, webhook_id: str, order_id: str, event_type: str, payload: str) -> bool:
        """Log webhook event"""
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
            INSERT INTO payment_webhooks (id, order_id, event_type, payload)
            VALUES (?, ?, ?, ?)
            """, (webhook_id, order_id, event_type, payload))
            
            conn.commit()
            return True
        except Exception as e:
            print(f"Error logging webhook: {e}")
            return False
        finally:
            conn.close()


order_manager = OrderManager()
