# 💰 DANA Payment Gateway Integration - Implementation Guide

Panduan lengkap untuk mengintegrasikan DANA Payment Gateway ke aplikasi Dokumen-Bengkel untuk monetisasi.

---

## 📋 Fitur yang Ditambahkan

### 1. **DANA Payment Gateway Integration** (`dana_payment.py`)
- OAuth2 authentication dengan DANA API
- Create payment orders
- Verify payment status
- Automatic token refresh

### 2. **Order Management System** (`order_manager.py`)
- Database schema untuk orders, transactions, webhooks
- Order creation dan tracking
- Payment status management
- Analytics support

### 3. **Payment Routes** (`payment_routes.py`)
- `POST /payment/docs/premium` - Create payment order
- `GET /payment/success/<order_id>` - Payment success callback
- `POST /payment/webhook/dana` - DANA webhook receiver
- `GET /payment/status/<order_id>` - Check payment status
- `GET /payment/orders?email=...` - Get user orders
- `GET /payment/analytics` - Payment analytics

### 4. **UI Templates**
- `premium.html` - Premium documents listing
- `payment_success.html` - Success page
- `payment_pending.html` - Pending page
- `payment_error.html` - Error page

---

## 🔧 Setup Instructions

### Step 1: Update app.py

Tambahkan ke file `app.py` setelah import statements:

```python
# Payment Gateway Integration
from order_manager import init_payment_db, order_manager
from payment_routes import init_payment_routes

# Initialize payment database
init_payment_db()

# Initialize payment routes
init_payment_routes(app)
```

Pastikan ditambahkan SEBELUM `if __name__ == '__main__':`

### Step 2: Set Environment Variables (Production)

Di PythonAnywhere atau production server, set environment variables:

```bash
export DANA_MERCHANT_ID="216620010026043209503"
export DANA_CLIENT_ID="2025112621324475258385"
export DANA_CLIENT_SECRET="0320254759fb001aa2f48b2f941949eb39a817758c949a391fbc6709ec738f3b"
export DANA_PUBLIC_KEY="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAw1kGzQWEKz9n1fBSLB0JLyknOejQcT6xCgSK0+PpAL+F2VfAIwZatlD7oGVFTeAA/g0esuRf8SEJ6mVCDdXQuauHeIKJYMYqrzoWr0B6j1GSjz0GgJ0ontPtLvfPgxI9qp5mafUzVq7iU9d6VGmk+hjCUbl2jHVgHmypwIbPwZ8tZ9uQi+Vq2gQXTMgCEljaX4GoBKkVgk5Iqv2csOz85QFFb5BHs/RE/anZLyVOwCaX2sI9GPIMMuvuAuHmI1ak2VaZ6YaAALUWGMVktZCRm10WcPlxe/j8mj/6IqmSU158tU6o4QuibWV7GkTMS3tI0o3HHgM2ixhmjX+ixQ/WfQIDAQAB"
export DANA_PRIVATE_KEY="MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDDWQbNBYQrP2fV8FIsHQkvKSc56NBxPrEKBIrT4+kAv4XZV8AjBlq2UPugZUVN4AD+DR6y5F/xIQnqZUIN1dC5q4d4golgxiqvOhavQHqPUZKPPQaAnSie0+0u98+DEj2qnmZp9TNWruJT13pUaaT6GMJRuXaMdWAebKnAhs/Bny1n25CL5WraBBdMyAISWNpfgagEqRWCTkiq/Zyw7PzlAUVvkEez9ET9qdkvJU7AJpfawj0Y8gwy6+4C4eYjVqTZVpnphoAAtRYYxWS1kJGbXRZw+XF7+PyaP/oiqZJTXny1TqjhC6JtZXsaRMxLe0jSjcceAzaLGGaNf6LFD9Z9AgMBAAECggEAVxElANhGkmgORcJ5PYQrhcOX4i2sSe0hR0/C+LIKNfUnGToNPw8j+0KZBGJew1jl2FXMqvsy7+xD2R8Mk9IK19Zl6QZ1aJaqi7MeTTo15g77fbA7Z7OkWTYn7tkwukC1D4jOKMfK/AWyhp/xvBHiID5MzdQVzIC8OJNCDbeIfclFyNTQxNwW835+Tv2D4rKJXUzz0wntkyWiF3dIwaJ4mQEPrLkObIcltwRxQE5fH643ZZ6rIZfONGObnc4GSxD0PM/F1eVXQxIn2U9N9KhsKtQuMlFkEacqJ8CWa7W5ZdMcvikSk7Xju/kT/urBZLaal0aMJcw9HmnSfmBTgZ9TGQKBgQDGEPX2L8YHodAb1mM2WdODvwufVlOU7ca1fPi0/QTMCG5aB6Fj+TEoM5z8/Wu1l3/WxjehcVpA5zbHCek4Nz0RyeuH5zGSbL/g49zSn/jSVlLcrWHALX8GgpQGdgeQyKyxx/u9d4aWAV+Z14RKfzrGf5SrhQV6w+FhsbAZS53QcwKBgQD8fIHaba2qfjc6Cvb0xSMyfChEzY3QrMK0UOfk1m1H4Xwb/wUs6eG/7FWHpiIkR66h6p0Bj8OL4HiygKSl63m5FL8qSeOmf1COln7hu6brXBqj/5PrrxlLcm0qBt3xYnrxHCS559L75N+CyJdQHCVPtB9Fl57c1KsZwCTZFo+xTwKBgFE4xVRmdOPOVGQF/3tbTKSbJG373ZyWAUWNcQPvOhddYbtjo6g2mRTuTXNljNTTwqXVdRysOiGhb1Ih21SlOlLgJcj+YtKz69+SMYzh8wx2P9ak9w/y2ENYKtGXdzTFRiRFaRNiP3umJokU2vgdwoGB8fqAOyYDy5nfXuKQoq/HAoGAAL9VmxHsC68n9rIFnR/gRMv9SobZPp7kTKhYp2LDHA1c0rBkkYd3tZu7fRVO0JCtwajyIgkM6SMW+GBNHHif+Z5IGpXxaJLD6EglxAFMMzIomgetpmr0Rjbmf9NZYNeLyZ7ttOcsxrYcu0Rgvkn3Ck9cMFaMj9bJUuAwu7vHXR0CgYBeERamMyDBiyJzFraopcxYod+4pOc838evJ5u8po0S9XZdNOAlcBotPoMZJJJOSmWY5EDSJWllSE6GAOY6TCAOPLMO7qkzwlA1xV7QP/kuN5FfLNggYjxFmcNFwKaXCxlOW0uaDDJY37yWWoQrWYdqGDgazSB0QovnfFw6CFKA5A=="
```

Atau di PythonAnywhere Bash Console:
```bash
cat >> ~/.bashrc << 'EOF'
export DANA_MERCHANT_ID="216620010026043209503"
export DANA_CLIENT_ID="2025112621324475258385"
export DANA_CLIENT_SECRET="0320254759fb001aa2f48b2f941949eb39a817758c949a391fbc6709ec738f3b"
EOF
```

### Step 3: Initialize Payment Database

Di Bash Console PythonAnywhere:
```bash
cd ~/Dokumen-Bengkel
workon dokumen-bengkel
python3 -c "from order_manager import init_payment_db; init_payment_db()"
```

Output: `✅ Payment database tables initialized`

### Step 4: Update app.py Imports

Buka `app.py` dan tambahkan di akhir file (sebelum `if __name__ == '__main__':`):

```python
# ===== PAYMENT GATEWAY INTEGRATION =====
from order_manager import init_payment_db, order_manager
from payment_routes import init_payment_routes

# Initialize payment database
try:
    init_payment_db()
except:
    pass  # Tables already exist

# Initialize payment routes
init_payment_routes(app)
```

### Step 5: Update Navigation Link

Edit `templates/base.html` atau `templates/index.html` dan tambahkan link:

```html
<a href="/payment/docs/premium" class="btn btn-success">
    💰 Premium Documents
</a>
```

### Step 6: Reload & Test

Di PythonAnywhere:
1. Tab "Web" → Klik tombol **"Reload"** 
2. Tunggu 15 detik
3. Kunjungi: `https://gazruxenginering.pythonanywhere.com/payment/docs/premium`

---

## 🧪 Testing di Sandbox

### Test Payment Flow

1. **Visit Premium Page**
   - URL: `https://gazruxenginering.pythonanywhere.com/payment/docs/premium`
   - Klik "Get Access" pada salah satu produk

2. **Enter Email**
   - Masukkan email test Anda
   - Klik "Proceed to Payment"

3. **DANA Payment**
   - Akan redirect ke DANA sandbox payment page
   - Gunakan test credentials dari DANA sandbox

4. **Webhook Verification**
   - DANA akan send webhook ke `/payment/webhook/dana`
   - System akan auto-update order status

### Test Credentials (Sandbox)

Gunakan test data DANA yang sudah disediakan di `dana_payment.py`

---

## 📊 Monitoring & Analytics

### Check Payment Status

```bash
# Via API
curl "https://gazruxenginering.pythonanywhere.com/payment/status/order_abc123"

# Get user orders
curl "https://gazruxenginering.pythonanywhere.com/payment/orders?email=user@example.com"

# Analytics
curl "https://gazruxenginering.pythonanywhere.com/payment/analytics"
```

### Database Queries

```bash
# Check orders
sqlite3 database.db "SELECT * FROM orders LIMIT 10;"

# Check transactions
sqlite3 database.db "SELECT * FROM transactions;"

# Revenue report
sqlite3 database.db "SELECT SUM(amount) as total FROM orders WHERE status = 'COMPLETED';"
```

---

## 🚀 Production Deployment

### 1. Update to Production DANA Credentials

Buka `dana_payment.py` dan ubah:
```python
DANA_CONFIG = {
    "production": {
        "base_url": "https://api.dana.id",  # Change from sandbox
        "merchant_id": "YOUR_PRODUCTION_MERCHANT_ID",
        ...
    }
}
```

### 2. Change Environment

Di `dana_payment.py` akhir file:
```python
dana_gateway = DANAPaymentGateway(environment="production")  # Change from sandbox
```

### 3. Update Webhook URLs

Update DNS/domain configuration agar DANA webhook bisa reach server Anda.

### 4. Enable HTTPS

Pastikan SSL/TLS aktif (PythonAnywhere auto-provide)

### 5. Test di Production

Gunakan production DANA credentials dan test minimal 5 transaksi sebelum go live

---

## 🐛 Troubleshooting

### Error: "Failed to get access token"

**Solusi:**
```bash
# Verify credentials
echo $DANA_CLIENT_ID
echo $DANA_CLIENT_SECRET

# Test API connectivity
curl -X POST https://api.sandbox.dana.id/oauth2/token \
  -d "grant_type=client_credentials&client_id=YOUR_ID&client_secret=YOUR_SECRET"
```

### Error: "Order not found"

**Solusi:**
```bash
# Check database
sqlite3 database.db "SELECT * FROM orders WHERE id LIKE 'order_%';"
```

### Webhook not received

**Solusi:**
1. Verify webhook URL is publicly accessible
2. Check firewall/network settings
3. Review webhook logs: `SELECT * FROM payment_webhooks;`

---

## 📈 Revenue Optimization Tips

1. **Dynamic Pricing**: Set berbagai price points untuk different customer segments
2. **Promotional Codes**: Tambahkan discount system
3. **Subscription Model**: Auto-recurring payments dengan DANA
4. **Bundle Deals**: Paket hemat untuk multiple documents
5. **Analytics**: Monitor which products generate most revenue

---

## 🔒 Security Checklist

- ✅ Never commit DANA credentials (use env vars)
- ✅ Validate webhook signatures
- ✅ Use HTTPS for all payment URLs
- ✅ Implement rate limiting on payment endpoints
- ✅ Log all transactions for audit trail
- ✅ Regular backups of payment database

---

## 📞 Support

- DANA API Docs: https://dana.id/api-documentation
- Technical Support: contact@dana.id

Good luck with your monetization! 🚀💰

