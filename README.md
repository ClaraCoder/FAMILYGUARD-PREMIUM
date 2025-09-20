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
