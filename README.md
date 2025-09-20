# FAMILYGUARD-PREMIUM
FAMILYGUARD PREMIUM (TERMUX)
Struktur Direktori dan File

```
familyguard/
├── app.py
├── config.json
├── requirements.txt
├── start.sh
├── setup_database.py
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── anak.html
│   ├── settings.html
│   └── alerts.html
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── dashboard.css
│   ├── js/
│   │   ├── script.js
│   │   ├── map.js
│   │   └── charts.js
│   └── img/
│       ├── logo.png
│       └── background.jpg
└── modules/
    ├── location_tracker.py
    ├── content_filter.py
    ├── screen_time.py
    └── alert_system.py

Langkah Pemasangan Manual di Termux

1. Persiapan Awal

```bash
# Update package list dan install dependencies
pkg update && pkg upgrade -y
pkg install python nodejs git wget curl openssl-tool proot make clang termux-api -y

# Install Python packages
pip install flask flask-cors requests pillow geopy cryptography pandas numpy matplotlib
```

2. Buat Struktur Direktori

```bash
# Buat direktori utama
mkdir ~/familyguard
cd ~/familyguard

# Buat subdirektori
mkdir -p templates static/css static/js static/img modules
```

** Jalankan Aplikasi **

Setelah semua file dibuat, jalankan perintah berikut:

```bash
# Setup database
cd ~/familyguard
python setup_database.py

# Jalankan aplikasi
python app.py
```

Aplikasi akan berjalan di http://localhost:5000. Gunakan password default family123 untuk login.

Fitur Premium FamilyGuard:

1. Dashboard Elegant - Antarmuka modern dengan statistik real-time
2. Pelacakan Lokasi Canggih - Dengan geofencing dan notifikasi
3. Manajemen Screen Time - Pantau dan batasi waktu layar
4. Filter Konten - Blokir konten tidak pantas
5. Sistem Alert - Notifikasi real-time untuk aktivitas mencurigakan
6. Laporan Detail - Analisis penggunaan perangkat
7. Multi-Device Support - Pantau beberapa perangkat sekaligus
8. Keamanan Tingkat Tinggi - Enkripsi data dan autentikasi aman
