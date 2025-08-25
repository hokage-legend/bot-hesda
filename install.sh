#!/bin/bash

# Skrip akan berhenti jika ada perintah yang gagal
set -e

# --- Variabel Konfigurasi ---
PROJECT_DIR="/root/bot-telegram"
SERVICE_NAME="telegram_bot.service"
SERVICE_FILE="/etc/systemd/system/$SERVICE_NAME"

# --- Mulai Instalasi ---
echo ">>> Memulai instalasi Telegram Bot..."

# 1. Pastikan skrip dijalankan sebagai root
if [ "$EUID" -ne 0 ]; then
  echo "Harap jalankan skrip ini sebagai root (gunakan sudo)."
  exit 1
fi

# 2. Update package list
echo ">>> [1/6] Melakukan update package list..."
apt-get update

# 3. Install paket yang dibutuhkan (python venv)
echo ">>> [2/6] Menginstall python3-Telegram-Bot..."
sudo pip install python-telegram-bot --break-system-packages

# 4. Menginstall dependencies dari requirements.txt
echo ">>> [4/6] Menginstall dependencies dari requirements.txt..."
source venv/bin/activate
pip install -r requirements.txt
deactivate

# 5. Membuat file layanan systemd
echo ">>> [5/6] Membuat file layanan systemd..."

# Bagian ini adalah perbaikan utamanya.
# Path ke main.py sekarang sudah benar menunjuk ke dalam folder 'bot'.
cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Telegram PPOB Reseller Bot
After=network.target

[Service]
User=root
WorkingDirectory=$PROJECT_DIR
ExecStart=/usr/bin/python3 /root/bot/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

echo "File layanan berhasil dibuat di $SERVICE_FILE"

# 7. Reload systemd dan jalankan service
echo ">>> [6/6] Me-reload systemd dan menjalankan layanan bot..."
systemctl daemon-reload
systemctl enable "$SERVICE_NAME"
systemctl restart "$SERVICE_NAME"

echo ""
echo ">>> Instalasi Selesai! Bot Anda sekarang seharusnya sudah berjalan."
echo ">>> Untuk memeriksa status bot, jalankan: sudo systemctl status $SERVICE_NAME"
echo ">>> Untuk melihat log bot secara live, jalankan: sudo journalctl -u $SERVICE_NAME -f"
