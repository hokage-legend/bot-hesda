from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# Inline keyboard untuk menu utama
MAIN_MENU_KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("💰 Cek Saldo", callback_data="cek_saldo"),
            InlineKeyboardButton("📦 Beli Paket", callback_data="buy_package_menu"),
        ],
        [
            InlineKeyboardButton("📈 Cek Status", callback_data="cek_status"),
            InlineKeyboardButton("🤝 Bantuan", callback_data="bantuan"),
        ],
        [
            InlineKeyboardButton("🧪 Lihat Semua Paket (Debug)", callback_data="lihat_semua_paket_0")
        ]
    ]
)

# Inline keyboard untuk menu pembelian, sekarang dengan kategori
BUY_MENU_KEYBOARD = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("🚀 Paket Utama", callback_data="category_utama")],
        [InlineKeyboardButton("➕ Paket Add-On", callback_data="category_addon")],
        [InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="back_to_main_menu")],
    ]
)

# Inline keyboard untuk tombol kembali
BACK_BUTTON_TO_MAIN = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Kembali ke Menu Utama", callback_data="back_to_main_menu")]]
)

# Inline keyboard untuk kembali ke menu pembelian
BACK_BUTTON_TO_BUY_MENU = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Kembali ke Menu Kategori", callback_data="buy_package_menu")]]
)


def create_product_list_keyboard(products, category):
    """Membuat keyboard inline dari daftar produk untuk kategori tertentu."""
    keyboard = []
    # Filter produk berdasarkan kategori yang diminta
    filtered_products = [p for p in products if p.get('category') == category]
    
    for product in filtered_products:
        # Menambahkan package_code ke callback_data untuk identifikasi
        button = InlineKeyboardButton(
            f"{product['package_name_show']} ({product['harga']})",
            callback_data=f"show_product_{product['package_code']}"
        )
        keyboard.append([button])
    
    # Tambahkan tombol kembali ke menu kategori
    keyboard.append([InlineKeyboardButton("🔙 Kembali ke Kategori", callback_data="buy_package_menu")])

    return InlineKeyboardMarkup(keyboard)

def create_pagination_keyboard(current_page, total_pages, callback_prefix):
    """Membuat keyboard dengan tombol navigasi (next/prev)."""
    keyboard_buttons = []
    
    if current_page > 0:
        keyboard_buttons.append(InlineKeyboardButton("⬅️ Sebelumnya", callback_data=f"{callback_prefix}_{current_page - 1}"))
    
    if current_page < total_pages - 1:
        keyboard_buttons.append(InlineKeyboardButton("Selanjutnya ➡️", callback_data=f"{callback_prefix}_{current_page + 1}"))
    
    keyboard = [keyboard_buttons]
    keyboard.append([InlineKeyboardButton("❌ Selesai", callback_data="back_to_main_menu")])

    return InlineKeyboardMarkup(keyboard)