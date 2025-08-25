import logging
import requests
from telegram import Update
from telegram.ext import ContextTypes

import config
from keyboards import MAIN_MENU_KEYBOARD, BACK_BUTTON_TO_MAIN
from pricelist_handler import handle_pricelist_callback

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menampilkan keyboard menu utama (inline) atau mengedit pesan yang ada."""
    if update.callback_query:
        query = update.callback_query
        await query.edit_message_text(
            "Halo! Silakan pilih salah satu menu di bawah ini:",
            reply_markup=MAIN_MENU_KEYBOARD
        )
    else:
        await update.message.reply_text(
            "Halo! Selamat datang di bot PPOB Hesda Store.\n\n"
            "Silakan pilih salah satu menu di bawah ini:",
            reply_markup=MAIN_MENU_KEYBOARD
        )

async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Router utama untuk semua callback query."""
    query = update.callback_query
    await query.answer()
    
    command = query.data
    
    # Perintah yang ditangani di handler utama
    if command == "cek_saldo":
        await cek_saldo(update, context)
    elif command == "back_to_main_menu":
        await start(update, context)
    
    # Delegasikan ke handler pricelist jika perintah berhubungan dengan paket atau debug
    elif command.startswith(("buy_package_", "category_", "show_product_", "lihat_semua_paket_")):
        await handle_pricelist_callback(update, context)
    
    # Tambahkan logika untuk tombol lain (Cek Status, Bantuan) di sini
    else:
        await query.edit_message_text(f"Menu '{command}' sedang dalam pengembangan.", reply_markup=BACK_BUTTON_TO_MAIN)


async def cek_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mengirimkan permintaan ke API untuk cek saldo dan merespons pengguna."""
    query = update.callback_query
    await query.edit_message_text("Sedang memeriksa saldo Anda...")
    
    try:
        url = f"{config.API_BASE_URL}saldo?hesdastore={config.HESDASTORE_KEY}"
        response = requests.get(url, auth=(config.EMAIL_ANDA, config.PASSWORD_ANDA))
        response.raise_for_status()
        data = response.json()
        
        if data['status']:
            saldo = data['data']['saldo']
            formatted_saldo = f"Rp {saldo:,.0f}".replace(",", ".")
            await query.edit_message_text(
                f"💰 Saldo Anda saat ini: *{formatted_saldo}*",
                parse_mode='Markdown',
                reply_markup=BACK_BUTTON_TO_MAIN
            )
        else:
            await query.edit_message_text(
                f"Gagal mengambil saldo. Pesan dari API: {data.get('message', 'Tidak ada pesan error.')}",
                reply_markup=BACK_BUTTON_TO_MAIN
            )
    except Exception as e:
        logger.error(f"Terjadi kesalahan di cek_saldo: {e}")
        await query.edit_message_text("Terjadi kesalahan tak terduga. Hubungi admin.", reply_markup=BACK_BUTTON_TO_MAIN)