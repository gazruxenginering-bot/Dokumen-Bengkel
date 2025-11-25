# PythonAnywhere Setup Guide - Google Drive File Browser

## 📋 Checklist Setup

- [ ] Step 1: Push GitHub
- [ ] Step 2: Create PythonAnywhere Web App
- [ ] Step 3: Clone Repository
- [ ] Step 4: Setup Virtual Environment
- [ ] Step 5: Configure WSGI
- [ ] Step 6: Setup Environment Variables
- [ ] Step 7: Reload & Test

---

## Step 1️⃣: Push Kode ke GitHub

**Di Replit Shell:**

```bash
cd /home/runner/workspace

# Setup git
git config user.name "Your Name"
git config user.email "your.email@gmail.com"

# Commit & push
git add .
git commit -m "Initial commit: Google Drive File Browser for PythonAnywhere"
git remote add origin https://github.com/YOUR_USERNAME/google-drive-browser.git
git branch -M main
git push -u origin main
```

**Catatan:** Saat diminta password, gunakan **Personal Access Token** dari GitHub (bukan password akun).

---

## Step 2️⃣: Buat Web App di PythonAnywhere

1. Login ke [pythonanywhere.com](https://www.pythonanywhere.com) dengan akun Anda
2. Klik tab **"Web"** (di sidebar sebelah kiri)
3. Klik **"Add a new web app"**
4. Pilih:
   - Domain: `gazruxenginering.pythonanywhere.com` (default)
   - Framework: **"Manual configuration"**
   - Python version: **"Python 3.11"** (or latest)
5. Klik **"Next"** → **"Finish"**

---

## Step 3️⃣: Clone Repository & Install Dependencies

Di PythonAnywhere, buka **Bash Console**:

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/google-drive-browser.git

# Navigate ke folder
cd google-drive-browser

# Install requirements
pip install -r requirements.txt
```

---

## Step 4️⃣: Setup Virtual Environment (Opsional tapi Recommended)

```bash
# Buat virtual environment
mkvirtualenv --python=/usr/bin/python3.11 google-drive

# Install di venv
pip install -r requirements.txt
```

**Kalau menggunakan venv, catat path:**
```
/home/gazruxenginering/.virtualenvs/google-drive
```

---

## Step 5️⃣: Configure WSGI File

1. Di PythonAnywhere, tab **"Web"** → cari **"WSGI configuration file"**
2. Edit file (path akan terlihat, misal: `/var/www/gazruxenginering_pythonanywhere_com_wsgi.py`)
3. Replace seluruh content dengan:

```python
import sys
import os

# Add project directory to path
project_dir = '/home/gazruxenginering/google-drive-browser'
if project_dir not in sys.path:
    sys.path.insert(0, project_dir)

# Set working directory
os.chdir(project_dir)

# If using virtual environment, uncomment:
# activate_this = '/home/gazruxenginering/.virtualenvs/google-drive/bin/activate_this.py'
# exec(open(activate_this).read())

# Import Flask app
from app import app as application
```

4. Save (Ctrl+S atau tombol Save)

---

## Step 6️⃣: Setup Environment Variables

1. Tab **"Web"** → scroll ke bawah → **"Environment variables"**
2. Click tombol edit/add
3. Tambahkan key-value:
   - **Key:** `SERVICE_ACCOUNT_JSON`
   - **Value:** Paste seluruh isi `credentials.json` (dari Replit)

**Cara dapatkan credentials:**
1. Di Replit, buka file `credentials.json`
2. Copy SELURUH isi (mulai `{` sampai `}`)
3. Paste di PythonAnywhere value field

---

## Step 7️⃣: Reload & Test

1. Tab **"Web"** → Klik tombol **"Reload"** (hijau)
2. Tunggu ~10 detik
3. Klik link website (misal: `https://gazruxenginering.pythonanywhere.com`)
4. Aplikasi seharusnya live! 🎉

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'flask'"
→ Pastikan install requirements di bash: `pip install -r requirements.txt`

### Error: "Google Drive connection failed"
→ Cek `SERVICE_ACCOUNT_JSON` di environment variables sudah correct

### Error: "404 Not Found"
→ Pastikan WSGI file sudah save dan reload di-click

### Aplikasi Lambat Saat Pertama Kali
→ Normal, tunggu ~30 detik, biasanya sudah cepat

---

## 📊 Informasi Berguna

| Aspek | Keterangan |
|-------|-----------|
| **URL Website** | `https://gazruxenginering.pythonanywhere.com` |
| **Bash Console** | Tab "Consoles" → "Bash" |
| **File Manager** | Tab "Files" |
| **Database** | Auto-created di `/home/gazruxenginering/google-drive/database.db` |
| **Logs** | Tab "Web" → "Error log" & "Server log" |
| **Sleep Mode** | Free tier sleep setelah 3 bulan inactivity |

---

## 🚀 Next Steps

1. ✅ Aplikasi live di `gazruxenginering.pythonanywhere.com`
2. ✅ Share URL ke teman/user untuk testing
3. Kalau mau always-on 24/7 → upgrade ke **Paid plan** ($5+/bulan)

---

## Butuh Bantuan?

- Error saat setup? Check logs di PythonAnywhere (Tab "Web" → scroll bawah)
- Database issue? Check di Tab "Databases" → "MySQL" (kalau perlu)
- Custom domain? Settings → "Web" tab (untuk Paid plan)

Selamat! 🎉
