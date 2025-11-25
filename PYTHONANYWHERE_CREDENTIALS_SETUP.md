# 🔑 Setup Credentials di PythonAnywhere

Karena PythonAnywhere free tier tidak memiliki Environment Variables UI, kita akan upload `credentials.json` langsung ke folder project.

---

## ✅ **Cara Upload credentials.json (2 Methods)**

### **Method 1: Via PythonAnywhere Files (EASIEST)**

1. **Buka Files Tab di PythonAnywhere**
   - Navigate ke: `/home/gazruxenginering/Dokumen-Bengkel/`

2. **Upload credentials.json**
   - Klik tombol **"Upload a file"** (kuning)
   - Pilih file `credentials.json` dari lokal
   - Upload

3. **Verify**
   - Pastikan file muncul di file list
   - Ukuran sekitar 2.4 KB

---

### **Method 2: Via Bash Console**

```bash
# 1. Masuk folder project
cd ~/Dokumen-Bengkel

# 2. Buat file credentials.json via nano
nano credentials.json

# 3. Paste isi credentials.json (copy dari lokal)
# Ctrl+Shift+V untuk paste
# Ctrl+X, Y, Enter untuk save

# 4. Verify
ls -la credentials.json
```

---

## 📝 **Isi credentials.json**

Anda bisa copy dari sini atau dari file lokal di workspace.

File lokal tersedia di: `/workspaces/Dokumen-Bengkel/credentials.json`

---

## ✅ **Setelah Upload:**

1. **Verify di Bash Console**
   ```bash
   cd ~/Dokumen-Bengkel
   head -5 credentials.json
   ```
   
   Seharusnya output:
   ```
   {
     "type": "service_account",
     "project_id": "studio-9399526178-46fef",
   ```

2. **Reload Web App**
   - Tab "Web" → Tombol "Reload"
   - Tunggu 10-15 detik

3. **Test Aplikasi**
   - Buka: https://gazruxenginering.pythonanywhere.com
   - Seharusnya halaman utama ter-load dengan 4 folder

---

## 🐛 **Troubleshooting**

### ❌ Error: "credentials.json not found"
**Solusi:**
```bash
# Cek file ada
ls -la ~/Dokumen-Bengkel/credentials.json

# Jika tidak ada, upload via Files atau Bash Console
```

### ❌ Error: "Invalid credentials"
**Solusi:**
1. Verifikasi credentials.json valid JSON
2. Buka file di PythonAnywhere Files
3. Cek isi sudah lengkap (dari `{` sampai `}`)
4. Reload web app

### ❌ Error: "Permission denied"
**Solusi:**
```bash
# Set permissions
chmod 600 ~/Dokumen-Bengkel/credentials.json
```

---

## ✨ **Done!**

Setelah credentials.json ada, aplikasi sudah ready untuk:
- ✅ Mengakses Google Drive
- ✅ Menampilkan folder & file
- ✅ Preview PDF
- ✅ Search functionality

🎉 Aplikasi siap digunakan!

