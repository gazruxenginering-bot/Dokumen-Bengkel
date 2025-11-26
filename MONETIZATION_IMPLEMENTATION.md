# 🚀 DANA Payment Integration - Implementation Checklist

Panduan step-by-step untuk implementasi DANA payment gateway ke aplikasi yang sudah berjalan.

---

## ✅ Pre-Implementation Checklist

- [x] DANA Sandbox Credentials sudah siap
- [x] Dokumen-Bengkel sudah deployed di PythonAnywhere
- [x] Payment modules sudah di-commit ke GitHub

---

## 📋 Implementation Steps (Urutan Penting!)

### **STEP 1: Update app.py** ⭐ CRITICAL

**File:** `/home/gazruxenginering/Dokumen-Bengkel/app.py`

**Lokasi:** Setelah import statements di awal file

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

**Tempat yang tepat:** Sebelum `if __name__ == '__main__':`

---

### **STEP 2: Pull Latest Code dari GitHub**

Di PythonAnywhere Bash Console:

```bash
cd ~/Dokumen-Bengkel
git pull origin main
```

Ini akan download:
- `dana_payment.py`
- `order_manager.py`
- `payment_routes.py`
- `templates/premium.html`, dll
- `MONETIZATION_GUIDE.md`

---

### **STEP 3: Initialize Payment Database**

Di Bash Console:

```bash
cd ~/Dokumen-Bengkel
workon dokumen-bengkel
python3 << 'EOF'
from order_manager import init_payment_db
init_payment_db()
print("✅ Payment database initialized!")
EOF
```

**Expected output:**
```
✅ Payment database tables initialized
✅ Payment database initialized!
```

---

### **STEP 4: Test Import Modules**

```bash
cd ~/Dokumen-Bengkel
workon dokumen-bengkel
python3 -c "
from dana_payment import dana_gateway
from order_manager import order_manager
from payment_routes import init_payment_routes
print('✅ All imports successful!')
"
```

---

### **STEP 5: Reload Web App**

Di PythonAnywhere:
1. Tab "Web"
2. Klik tombol **"Reload"** (hijau)
3. Tunggu 15-30 detik

---

### **STEP 6: Test Payment Page**

Buka browser:
```
https://gazruxenginering.pythonanywhere.com/payment/docs/premium
```

**Expected:** Halaman dengan 3 produk premium muncul ✅

---

### **STEP 7: Test Payment Flow (Sandbox)**

1. Klik "Get Access" pada salah satu produk
2. Masukkan email Anda
3. Klik "Proceed to Payment"
4. Seharusnya redirect ke DANA payment page

---

## 🔧 Troubleshooting

### Error: "No module named 'dana_payment'"

**Solusi:**
```bash
cd ~/Dokumen-Bengkel
ls -la dana_payment.py
git pull origin main
```

### Error: "Syntax error in app.py"

**Solusi:**
- Pastikan kode ditambah dengan indentation yang benar
- Check syntax: `python3 -m py_compile app.py`

### Payment page tidak muncul

**Solusi:**
```bash
# Test payment routes import
python3 -c "from payment_routes import payment_bp; print('✅ Routes OK')"

# Check error log di PythonAnywhere
# Tab "Web" → Error log
```

### Database initialization error

**Solusi:**
```bash
# Reset database (WARNING: deletes all payment data!)
rm database.db
python3 -c "from order_manager import init_payment_db; init_payment_db()"
```

---

## 📊 Verification Checklist

Setelah implementasi, verifikasi:

- [ ] Payment page accessible di `/payment/docs/premium`
- [ ] Premium product cards displayed dengan benar
- [ ] Klik "Get Access" membuka modal dengan form email
- [ ] Form submit redirect ke DANA sandbox
- [ ] Database tables created: `sqlite3 database.db ".tables"`
- [ ] Error log di PythonAnywhere clean (no Python errors)

---

## 🧪 Full Test Scenario

### Scenario 1: Successful Payment

1. Open `/payment/docs/premium`
2. Pilih product "Premium Document Bundle 1"
3. Enter email: `test@example.com`
4. Proceed to payment
5. Complete payment di DANA sandbox
6. Should redirect to success page
7. Check database: `SELECT * FROM orders WHERE status = 'COMPLETED';`

### Scenario 2: Failed Payment

1. Same as above but cancel payment at DANA
2. Should show pending page
3. Check database: `SELECT * FROM orders WHERE status = 'PENDING';`

### Scenario 3: Check Order Status

```bash
curl "https://gazruxenginering.pythonanywhere.com/payment/status/order_xyz123"
```

---

## 🚀 Next Steps (Optional Enhancements)

1. **Add to Navigation Menu:**
   - Edit `templates/base.html`
   - Tambahkan link ke `/payment/docs/premium`

2. **Custom Pricing:**
   - Edit product list di `payment_routes.py`
   - Ubah harga sesuai kebutuhan

3. **Email Notifications:**
   - Integrasikan dengan email service (SendGrid, etc.)
   - Send receipt & access details otomatis

4. **Analytics Dashboard:**
   - Built-in analytics di `/payment/analytics`
   - Monitor revenue real-time

5. **Advanced Features:**
   - Subscription/recurring payments
   - Discount codes
   - Invoice management
   - Customer portal

---

## 📞 Quick Support

| Problem | Solution |
|---------|----------|
| Module not found | `git pull origin main` |
| Syntax error | `python3 -m py_compile app.py` |
| Database error | Check permissions: `ls -la database.db` |
| Payment not working | Check error log di PythonAnywhere |
| Webhook issues | Check firewall & HTTPS |

---

## ⏱️ Estimated Timeline

- Step 1-2: 5 minutes
- Step 3-5: 10 minutes
- Step 6-7: 5 minutes

**Total: ~20 minutes to full setup** ⚡

---

## 🎉 Success Indicators

Ketika implementasi berhasil:

✅ Premium page muncul dengan 3 produk
✅ Payment modal berfungsi  
✅ DANA redirect terjadi
✅ Order recorded di database
✅ No Python errors di error log
✅ Webhooks received & processed

**Congratulations! You're ready to monetize! 💰**

---

**Questions?** Check `MONETIZATION_GUIDE.md` untuk detail lebih lanjut.

