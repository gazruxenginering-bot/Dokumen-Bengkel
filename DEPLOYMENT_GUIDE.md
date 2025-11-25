# 🚀 Panduan Deployment ke PythonAnywhere

Dokumen ini adalah panduan **lengkap dan terstruktur** untuk mendeploy aplikasi Dokumen-Bengkel ke PythonAnywhere.

---

## 📋 Daftar Checklist

- [ ] **Langkah 1**: GitHub repository siap (secrets sudah di-approve)
- [ ] **Langkah 2**: Buat Web App di PythonAnywhere
- [ ] **Langkah 3**: Clone repository di PythonAnywhere
- [ ] **Langkah 4**: Setup Virtual Environment
- [ ] **Langkah 5**: Konfigurasi WSGI file
- [ ] **Langkah 6**: Setup Environment Variables
- [ ] **Langkah 7**: Reload & Test aplikasi

---

## 📌 Informasi Akun

| Item | Value |
|------|-------|
| **Akun PythonAnywhere** | gazruxenginering |
| **Domain URL** | https://gazruxenginering.pythonanywhere.com |
| **GitHub Repository** | https://github.com/gazruxenginering-bot/Dokumen-Bengkel |
| **Branch** | main |

---

## ✅ Langkah 1: GitHub - Approve Secrets (Jika diminta)

Jika GitHub menampilkan pesan "Push blocked - secrets detected":

1. Buka notifikasi dari GitHub
2. Klik link untuk "Review blocked push"
3. Klik "Allow" untuk mengijinkan secrets di repository
4. Kemudian retry push dari terminal

**Atau gunakan command ini:**
```bash
git push origin main --force-with-lease
```

---

## 🔧 Langkah 2: Buat Web App di PythonAnywhere

1. **Login ke PythonAnywhere:**
   - Buka https://www.pythonanywhere.com/user/gazruxenginering/
   - Login dengan akun Anda

2. **Buat Web App:**
   - Klik tab **"Web"** (sidebar kiri)
   - Klik **"Add a new web app"**
   - Pilih opsi:
     - Framework: **Manual configuration**
     - Python version: **Python 3.11** (atau versi terbaru)
   - Klik **Next** → **Finish**

3. **Catat Path WSGI file:**
   - Biasanya: `/var/www/gazruxenginering_pythonanywhere_com_wsgi.py`
   - Ini akan kita edit di Langkah 5

---

## 📁 Langkah 3: Clone Repository di PythonAnywhere

1. **Buka Bash Console:**
   - Di PythonAnywhere, klik tab **"Consoles"** → **"Bash"**
   - Atau buka console di tab "Web"

2. **Jalankan commands:**

```bash
# Clone repository ke home folder
cd ~
git clone https://github.com/gazruxenginering-bot/Dokumen-Bengkel.git

# Masuk folder
cd Dokumen-Bengkel

# Verifikasi folder structure
ls -la
```

3. **Verifikasi hasil:**
```
app.py
config.py
credentials.json
requirements.txt
templates/
... (file lainnya)
```

---

## 🐍 Langkah 4: Setup Virtual Environment (Recommended)

**Jalankan di Bash Console PythonAnywhere:**

```bash
# Buat virtual environment dengan Python 3.11
mkvirtualenv --python=/usr/bin/python3.11 dokumen-bengkel

# Virtual environment otomatis active, install dependencies
pip install -r requirements.txt
```

**Catat path venv:**
```
/home/gazruxenginering/.virtualenvs/dokumen-bengkel
```

---

## ⚙️ Langkah 5: Konfigurasi WSGI File

1. **Di PythonAnywhere, tab "Web":**
   - Scroll ke bagian **"Code"**
   - Cari **"WSGI configuration file"**
   - Klik path file tersebut untuk edit (biasanya `/var/www/gazruxenginering_pythonanywhere_com_wsgi.py`)

2. **Replace SELURUH isi file dengan:**

```python
"""
PythonAnywhere WSGI Configuration for Dokumen-Bengkel
"""

import sys
import os

# Add project directory to path
project_dir = '/home/gazruxenginering/Dokumen-Bengkel'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set working directory
os.chdir(project_dir)

# Activate virtual environment
activate_this = '/home/gazruxenginering/.virtualenvs/dokumen-bengkel/bin/activate_this.py'
try:
    exec(open(activate_this).read())
except:
    pass  # If venv activation fails, continue anyway

# Import Flask app
from app import app as application
```

3. **Save file** (Ctrl+S atau tombol Save di editor)

---

## 🔐 Langkah 6: Setup Environment Variables

1. **Di PythonAnywhere, tab "Web":**
   - Scroll ke bagian **"Environment variables"**
   - Klik tombol **Edit** atau **Add new variable**

2. **Tambahkan variable:**

   **Name:** `SERVICE_ACCOUNT_JSON`
   
   **Value:** (Paste seluruh isi `credentials.json` dari project)

   **Cara dapatkan:**
   - Buka file `credentials.json` di workspace lokal
   - Copy SELURUH isi (dari `{` sampai `}`)
   - Paste di value field PythonAnywhere

3. **Tambahkan variable (Optional):**

   **Name:** `FLASK_ENV`
   
   **Value:** `production`

4. **Save** perubahan

---

## 🔄 Langkah 7: Reload & Test Aplikasi

1. **Reload Web App:**
   - Di tab "Web", cari tombol **"Reload"** (hijau)
   - Klik tombol tersebut
   - Tunggu ~10-15 detik untuk reload

2. **Buka URL aplikasi:**
   - Klik link domain: https://gazruxenginering.pythonanywhere.com
   - atau ketik manual di browser

3. **Verifikasi aplikasi:**
   - ✅ Halaman utama ter-load
   - ✅ Folder root terlihat (EBOOKS, Pengetahuan, Service Manual 1, Service Manual 2)
   - ✅ Bisa klik folder dan lihat file
   - ✅ Search functionality berfungsi
   - ✅ PDF preview berfungsi

---

## 🐛 Troubleshooting

### ❌ Error 500 - Internal Server Error

**Solusi:**
1. Klik tab **"Web"** di PythonAnywhere
2. Scroll ke bawah, lihat **"Error log"**
3. Baca error message dan cari penyebabnya

**Common issues:**
- Module not found → `pip install -r requirements.txt` belum dijalankan
- credentials.json not found → SERVICE_ACCOUNT_JSON env var belum diset
- Permission denied → Check folder permissions

### ❌ ModuleNotFoundError

**Solusi:**
```bash
# Di Bash Console PythonAnywhere
workon dokumen-bengkel  # Activate venv
pip install -r requirements.txt
```

### ❌ "Static files not loading" / CSS/JS missing

**Solusi:**
1. Tidak perlu static files configuration untuk Flask default
2. CSS/JS di-serve dari templates
3. Jika perlu static files, tambahkan ke WSGI config:
   ```python
   from werkzeug.middleware.shared_data import SharedDataMiddleware
   application = SharedDataMiddleware(application, {
       '/static': '/home/gazruxenginering/Dokumen-Bengkel/static'
   })
   ```

### ❌ 502 Bad Gateway

**Solusi:**
1. Reload lagi via tombol "Reload"
2. Check error log
3. Verifikasi credentials.json valid

### ❌ Aplikasi lambat saat pertama kali dibuka

**Ini normal!** Cold start di PythonAnywhere bisa sampai 30 detik. Tunggu saja.

---

## 📊 Monitoring & Maintenance

### Cek Log Error:
- Tab "Web" → "Error log" (tail real-time)
- Refresh halaman untuk generate logs

### Cek Server Activity:
- Tab "Web" → "Server log"
- Lihat request history

### Update Aplikasi:
```bash
# Di Bash Console
cd ~/Dokumen-Bengkel
git pull origin main
# Tidak perlu reload jika hanya data/template berubah
# Reload jika app.py berubah
```

### Restart Aplikasi:
- Tab "Web" → Klik tombol **"Reload"**

---

## ✨ Advanced (Optional)

### Custom Domain
- Upgrade ke Paid plan ($5+/bulan)
- Tab "Web" → "Web app settings"
- Tambahkan custom domain

### Always-on Web App
- Upgrade ke Paid plan
- Cegah timeout saat aplikasi idle
- Default free tier: 3 bulan inactivity = app sleep

### Database Backup
- Automatic backup setiap hari
- Manual download di Tab "Files" → `/home/gazruxenginering/Dokumen-Bengkel/database.db`

---

## 🎉 Selesai!

Aplikasi Dokumen-Bengkel sekarang **LIVE** di:
### 👉 https://gazruxenginering.pythonanywhere.com 👈

---

## 📞 Butuh Bantuan?

Jika ada masalah:
1. **Check PythonAnywhere logs** (selalu mulai dari sini)
2. **Verify environment variables** sudah benar
3. **Test credentials.json** valid di Google Drive
4. Hubungi support PythonAnywhere jika perlu

**Good luck! 🚀**
