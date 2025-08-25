from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Keyboard untuk memilih jenis paket
PAKET_MENU_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("📦 Paket Non-OTP", callback_data="list_paket_nonotp"),
            InlineKeyboardButton("🔑 Paket OTP", callback_data="list_paket_otp"),
        ],
        [
            InlineKeyboardButton("❌ Paket Unreg", callback_data="list_paket_unreg")
        ],
    ]
)

# Keyboard untuk menu manajemen akrab (sesuai dokumentasi)
AKRAB_MENU_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("Pengelola", callback_data="akrab_pengelola"),
         InlineKeyboardButton("Anggota", callback_data="akrab_anggota")],
        [InlineKeyboardButton("Cek Stok Akrab", callback_data="akrab_cek_stok")],
    ]
)