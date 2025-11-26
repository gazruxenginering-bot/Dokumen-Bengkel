# 🔐 Admin Panel - User & Payment Monitoring

Panduan lengkap untuk menggunakan Admin Panel untuk monitoring users dan payments.

---

## 📊 Fitur Admin Panel

### **1. Dashboard Overview**
- Total revenue & today's revenue
- Total users & active customers  
- Order statistics (completed, pending, failed)
- Conversion rate & average order value
- Recent orders list
- Top-selling products

### **2. Users Management**
- List semua users dengan purchase history
- Top customers ranking
- User detail profile dengan order history
- Total spent per user
- First & last purchase tracking

### **3. Orders Management**
- All orders dengan status tracking
- Status summary (Completed/Pending/Failed)
- Order details & customer info
- Filter by date & status

### **4. Reports & Analytics**
- Revenue trend chart (30 days)
- Product performance analysis
- Sales by product
- CSV export untuk data analysis

---

## 🔑 Setup Admin Access

### **Step 1: Set Admin Password**

**Option A - Via Environment Variable (Recommended):**

```bash
export ADMIN_PASSWORD="YOUR_SECURE_PASSWORD"
```

**Option B - Edit admin_routes.py:**

```python
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'your_password_here')
```

⚠️ **SECURITY:** Ganti `admin123` dengan password yang kuat!

---

### **Step 2: Update app.py**

Tambahkan sebelum `if __name__ == '__main__':`

```python
# ===== ADMIN PANEL =====
from admin_dashboard import admin_dashboard
from admin_routes import init_admin_routes

# Initialize admin routes
init_admin_routes(app)
```

---

### **Step 3: Reload Web App**

Di PythonAnywhere:
1. Tab "Web"
2. Klik tombol **"Reload"**
3. Tunggu 15 detik

---

## 🚀 Accessing Admin Panel

### **URL:**
```
https://gazruxenginering.pythonanywhere.com/admin/login
```

### **Login:**
1. Enter password Anda
2. Klik "Login to Admin"

### **Dashboard Pages:**

| Page | URL | Purpose |
|------|-----|---------|
| Dashboard | `/admin/dashboard` | Overview & stats |
| Users | `/admin/users` | User management |
| User Detail | `/admin/user/<email>` | Individual user profile |
| Orders | `/admin/orders` | Orders list |
| Reports | `/admin/reports` | Analytics & charts |
| Export | `/admin/export/orders.csv` | Download CSV |

---

## 📊 Understanding the Dashboard

### **Stats Cards:**

**Total Revenue** - Cumulative revenue dari semua completed orders
- Showing: Total + Today's revenue

**Total Users** - Unique customers yang sudah melakukan purchase

**Completed Orders** - Successful transactions vs total orders
- Showing: Conversion rate percentage

**Avg Order Value** - Average purchase amount
- Showing: Pending orders count

---

### **Recent Orders Table:**

| Column | Description |
|--------|-------------|
| Order ID | Unique order identifier (last 8 chars) |
| Email | Customer email |
| Product | Product purchased |
| Amount | Transaction amount in IDR |
| Status | Order status (Completed/Pending/Failed) |
| Date | Order creation date |

---

## 👥 Users Management Features

### **Top Customers:**
- Ranked by total spending
- Shows order count & last order date
- Quick link to user profile

### **All Users List:**
- Purchase count
- Total spending
- First & last purchase dates
- Status distribution

### **User Detail Profile:**
- User email & summary stats
- Complete order history
- Order-by-order breakdown
- Export user data if needed

---

## 📋 Orders Management

### **Status Summary Cards:**
- **COMPLETED** - Successful payments (counted in revenue)
- **PENDING** - Awaiting payment verification
- **FAILED** - Payment failed or cancelled

### **Orders Table Features:**
- Sort by order ID, email, amount, status
- Click customer email → View user profile
- Filter by date range (future enhancement)

---

## 📈 Reports & Analytics

### **Revenue Trend Chart:**
- 30-day revenue visualization
- Line chart showing daily revenue
- Hover for detailed stats

### **Revenue Table:**
- Daily breakdown
- Orders & completed count
- Total revenue per day

### **Product Performance:**
- Sales by product
- Completed orders count
- Total & average price
- Percentage of total revenue (visual bar)

---

## 💾 Data Export

### **CSV Export:**

```
GET /admin/export/orders.csv?password=YOUR_PASSWORD
```

**Content:**
```
Order ID,Email,Product,Amount,Status,Created,Completed
order_abc123,user@example.com,Premium Bundle 1,50000,COMPLETED,2025-11-26 10:30:00,2025-11-26 10:35:00
...
```

**Usage:**
1. Download CSV file
2. Import ke Excel/Google Sheets
3. Analyze dengan pivot tables, charts, dll

---

## 🔒 Security Best Practices

✅ **DO:**
- Use strong, unique admin password
- Change password regularly
- Monitor admin login attempts
- Use HTTPS for all access
- Restrict admin URL with firewall rules

❌ **DON'T:**
- Share admin password
- Use default/simple passwords
- Access admin on public WiFi
- Leave admin logged in

---

## 🧪 Testing Admin Panel

### **Test Scenario 1: View Dashboard**
1. Login ke `/admin/login`
2. Navigate `/admin/dashboard`
3. Verify stats displayed correctly

### **Test Scenario 2: Check Users**
1. Go to `/admin/users`
2. Verify user list populated
3. Click user → View detail profile
4. Check order history

### **Test Scenario 3: View Orders**
1. Go to `/admin/orders`
2. Verify orders table populated
3. Check status distribution cards
4. Click customer email → View profile

### **Test Scenario 4: Analyze Reports**
1. Go to `/admin/reports`
2. Verify revenue chart displayed
3. Check product sales table
4. Export CSV

---

## 📞 API Endpoints

### **Get Dashboard Stats:**
```
GET /admin/api/stats?password=YOUR_PASSWORD
```

**Response:**
```json
{
  "total_revenue": 500000,
  "today_revenue": 50000,
  "total_users": 15,
  "total_orders": 20,
  "completed_orders": 18,
  "conversion_rate": 90.0,
  "avg_order_value": 27777.78
}
```

### **Get Revenue Data:**
```
GET /admin/api/revenue?days=30&password=YOUR_PASSWORD
```

### **Get Users List:**
```
GET /admin/api/users?limit=50&password=YOUR_PASSWORD
```

---

## 🚀 Future Enhancements

### **Planned Features:**
- [ ] Real-time dashboard updates (WebSocket)
- [ ] Advanced filtering & search
- [ ] Date range selection
- [ ] Multi-admin support with roles
- [ ] Email notifications for high-value orders
- [ ] Refund management interface
- [ ] Customer segmentation
- [ ] Revenue forecasting

---

## 🐛 Troubleshooting

### Error: "Invalid password"
- Verify password benar
- Check environment variable: `echo $ADMIN_PASSWORD`

### Error: "No data displayed"
- Check database has orders: `sqlite3 database.db "SELECT COUNT(*) FROM orders;"`
- Verify app.py sudah initialize admin routes

### Charts not showing
- Ensure Chart.js CDN accessible
- Check browser console for errors
- Verify data format valid

---

## 📊 Sample Dashboard Queries

Jika ingin manual query database:

```bash
# Total revenue
sqlite3 database.db "SELECT SUM(amount) FROM orders WHERE status='COMPLETED';"

# Users count
sqlite3 database.db "SELECT COUNT(DISTINCT user_email) FROM orders;"

# Revenue by day
sqlite3 database.db "SELECT DATE(created_at), SUM(amount) FROM orders WHERE status='COMPLETED' GROUP BY DATE(created_at);"

# Top products
sqlite3 database.db "SELECT product_name, COUNT(*), SUM(amount) FROM orders WHERE status='COMPLETED' GROUP BY product_id ORDER BY SUM(amount) DESC;"
```

---

## 🎯 Next Steps

1. ✅ Setup admin password
2. ✅ Update app.py with admin routes
3. ✅ Reload web app
4. ✅ Test admin login
5. ✅ Create some test orders
6. ✅ Monitor payments via admin panel
7. ✅ Export data for analysis

---

**Happy monitoring! 📊**

