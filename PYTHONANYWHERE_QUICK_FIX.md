# 🔧 PythonAnywhere - Quick Fix Commands

Jika mendapat error `requirements.txt` tidak ketemu, gunakan command ini di **Bash Console PythonAnywhere**:

---

## ❌ Command yang SALAH (Error):
```bash
pip install -r requirements.txt
```
Alasan: Anda tidak di folder project

---

## ✅ Command yang BENAR:

### **Option 1: Clone dulu (Recommended)**

```bash
# Masuk home folder
cd ~

# Clone repository
git clone https://github.com/gazruxenginering-bot/Dokumen-Bengkel.git

# Masuk folder
cd Dokumen-Bengkel

# List files untuk verifikasi
ls -la requirements.txt

# Buat virtual environment
mkvirtualenv --python=/usr/bin/python3.10 dokumen-bengkel

# Install requirements
pip install -r requirements.txt
```

---

### **Option 2: Jika sudah ada folder Dokumen-Bengkel**

```bash
# Masuk folder yang sudah ada
cd ~/Dokumen-Bengkel

# List untuk cek
ls -la requirements.txt

# Activate venv jika sudah ada
workon dokumen-bengkel

# Install requirements
pip install -r requirements.txt
```

---

## 📋 Step-by-Step di PythonAnywhere Bash Console:

1. **Lihat status folder:**
   ```bash
   pwd
   ls -la
   ```

2. **Jika belum ada Dokumen-Bengkel:**
   ```bash
   cd ~
   git clone https://github.com/gazruxenginering-bot/Dokumen-Bengkel.git
   cd Dokumen-Bengkel
   ```

3. **Buat venv:**
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 dokumen-bengkel
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Verifikasi berhasil:**
   ```bash
   python3 -c "import flask; import google.auth; print('✅ All imports OK')"
   ```

---

## ✅ Expected Output

Jika semuanya benar, akan lihat:
```
Successfully installed Flask-3.1.0 gunicorn-23.0.0 ...
✅ All imports OK
```

---

## 🆘 Jika Masih Error

1. **Cek posisi folder:**
   ```bash
   pwd
   ls -la requirements.txt
   ```

2. **Cek venv active:**
   ```bash
   which python3
   pip --version
   ```

3. **Jika venv belum active, activate:**
   ```bash
   workon dokumen-bengkel
   ```

4. **Coba install lagi:**
   ```bash
   pip install -r requirements.txt
   ```

---

Setelah semua ini selesai, lanjut ke langkah **Konfigurasi WSGI file**!
