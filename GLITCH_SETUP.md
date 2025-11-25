# Setup Glitch - Panduan Lengkap

## Langkah 1: Persiapkan GitHub Repository

### 1a. Setup Git (jika belum)
```bash
git init
git add .
git commit -m "Initial commit: Google Drive File Browser"
```

### 1b. Push ke GitHub
1. Buat repository baru di [github.com](https://github.com/new)
   - Nama: `google-drive-browser` (atau nama lain)
   - Jangan tambahkan README/LICENSE (kita sudah punya)
   - Click "Create repository"

2. Dari folder project Anda, jalankan:
```bash
git remote add origin https://github.com/YOUR_USERNAME/google-drive-browser.git
git branch -M main
git push -u origin main
```

---

## Langkah 2: Setup di Glitch

### 2a. Daftar & Login Glitch
1. Buka [glitch.com](https://glitch.com)
2. Klik "Sign up with GitHub" (gratis, tanpa kartu kredit)

### 2b. Import dari GitHub
1. Click "New Project" (tombol + di pojok kiri)
2. Pilih "Import from GitHub"
3. Paste URL repository Anda:
   ```
   https://github.com/YOUR_USERNAME/google-drive-browser
   ```
4. Click "Import"
5. Tunggu Glitch clone & setup (±1-2 menit)

---

## Langkah 3: Setup Environment Variables

Ini **PENTING** karena credentials.json tidak di-push ke GitHub!

1. Di Glitch, klik tombol `.env` (di sidebar kiri)
2. Tambahkan:

```env
SERVICE_ACCOUNT_JSON={"type":"service_account","project_id":"studio-9399526178-46fef",...}
```

**Untuk mendapatkan SERVICE_ACCOUNT_JSON:**

1. Buka file `credentials.json` di Replit
2. Copy **SELURUH** content file
3. Paste di Glitch .env sebagai `SERVICE_ACCOUNT_JSON=...`

---

## Langkah 4: Verifikasi & Jalankan

1. Glitch otomatis jalankan `npm install` dan app
2. Lihat logs di bawah (pastikan tidak ada error)
3. Klik tombol "Show" di atas → "Open in new window"
4. Aplikasi Anda live di: `https://your-project-name.glitch.me`

---

## ⚠️ Catatan Penting

- **database.db**: Akan auto-created di Glitch
- **Sleep mode**: Glitch free tier akan "sleep" kalau idle 15 menit, tapi bangun lagi saat ada akses
- **Storage**: Database hilang saat Glitch restart (jika mau persist, upgrade ke Glitch Paid)
- **Akses**: URL Glitch public & bisa dibagikan ke siapa saja

---

## Troubleshooting

### Error: "ModuleNotFoundError"
→ Klik "Logs" di Glitch, cek error message, pastikan environment var sudah di .env

### Error: "Google Drive Connection Failed"
→ Pastikan SERVICE_ACCOUNT_JSON di .env correct dan lengkap

### Aplikasi Lambat
→ Normal di Glitch free tier, tunggu 15 detik pertama kali loading

---

## Next Steps (Opsional)

Untuk production yang lebih reliable:
- Upgrade ke **Glitch Paid** ($5/bulan) untuk always-on
- Atau gunakan **Render.com** free tier (similar dengan Glitch)

Selamat! 🎉
