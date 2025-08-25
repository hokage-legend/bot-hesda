import logging
import requests
import math
from telegram import Update
from telegram.ext import ContextTypes

# Impor konfigurasi dan keyboard
import config
from keyboards import BUY_MENU_KEYBOARD, BACK_BUTTON_TO_MAIN, BACK_BUTTON_TO_BUY_MENU, create_product_list_keyboard, create_pagination_keyboard

# Inisialisasi logger
logger = logging.getLogger(__name__)

# =======================================================
# DAFTAR PRODUK LENGKAP ANDA DENGAN KATEGORI
# =======================================================
MY_PRODUCT_LIST = [
    # --- KATEGORI UTAMA ---
    {
        "package_name_show": "Masa Aktif XL 1 Tahun [45GB Setahun]",
        "package_code": "1447d54e21d581c9fb340e1cbf4e8fca", "package_id": "RjFNd09ZVWdsQVhQRHRQMWk0bnFxQQ",
        "harga": "Rp. 5.000", "jenis": "otp", "category": "utama"
    },
    {
        "package_name_show": "Masa Aktif XL 1 Tahun Alternatif",
        "package_code": "b0012edd21983678eb7ebc08d8f04ecd", "package_id": "ZkM1Z2duQm11SnBIZ003KytPeHFEdw",
        "harga": "Rp. 7.000", "jenis": "otp", "category": "utama"
    },
    {
        "package_name_show": "Xtra Unlimited Turbo Vidio - PULSA",
        "package_code": "XLUNLITURBOVIDIO_PULSA", "package_id": "MTJLR28vN3VpUmxObFdHelZwRnVUUQ",
        "harga": "Rp. 1.500", "jenis": "otp", "category": "utama"
    },
    {
        "package_name_show": "Xtra Unlimited Turbo Vidio - DANA/Qris",
        "package_code": "XLUNLITURBOVIDIO_DANA", "package_id": "ZVdMVXcyKzdJRlJERVdJc1hpVUhmQQ",
        "harga": "Rp. 1.500", "jenis": "otp", "category": "utama"
    },
    # --- KATEGORI ADD-ON ---
    {
        "package_name_show": "Addon Unlimited Turbo iFlix - Dana/Qris",
        "package_code": "XLUNLITURBOIFLIXXC_EWALLET", "package_id": "RFA2bTUzei82RUhieGxZamZCN21ndw",
        "harga": "Rp. 1.500", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "Addon Unlimited Turbo iFlix - Pulsa",
        "package_code": "XLUNLITURBOIFLIXXC_PULSA", "package_id": "aXdNcGhQSkswTy9rMmlpZ1BORWxBQQ",
        "harga": "Rp. 1.500", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Addon Unlimited Turbo Joox - Pulsa",
        "package_code": "XLUNLITURBOJOOXXC_PULSA", "package_id": "VlNxbzdGbDRtVnZHUmdwb284R2wzdw",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Addon Unlimited Turbo Netflix - Pulsa",
        "package_code": "XLUNLITURBONETFLIXXC_PULSA", "package_id": "MnFpMjJHaXhpU2pweUZ2WWRRM0tYZw",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Xtra Unlimited Turbo TikTok - Pulsa",
        "package_code": "XLUNLITURBOTIKTOK_PULSA", "package_id": "dlZJSi9kRC85U2tuc3ZaQkVmc1lkQQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Xtra Unlimited Turbo Viu - Pulsa",
        "package_code": "XLUNLITURBOVIU_PULSA", "package_id": "Tm8vcWtGQ01Kc3h1dlFFdGZqQ3FzUQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Addon Unlimited Turbo Netflix - Dana/Qris",
        "package_code": "XLUNLITURBONETFLIXXC", "package_id": "dXVnTG9SR0JpUC9pUVRLc1dPTTBpUQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Addon Unlimited Turbo Viu - Dana/Qris",
        "package_code": "XLUNLITURBOVIUXC", "package_id": "eW14MHdjem9Nc1lBYmtidGtyS2d4Zw",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Addon Unlimited Turbo Joox - Dana/Qris",
        "package_code": "XLUNLITURBOJOOXXC", "package_id": "SGRNN2d5ZnBXMDlFYlNRZ3psakZkUQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V2 Addon Unlimited Turbo TikTok - Qris/Dana",
        "package_code": "XLUNLITURBOTIKTOKXC", "package_id": "ZDRHc3JDVFFETWpiRzdBUEl6ZkEzdw",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Basic - Pulsa",
        "package_code": "XLUNLITURBOHBASIC7H_P", "package_id": "bStlR1JhcUkrZzlhYmdURWRMNUlaQQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Standard - Pulsa",
        "package_code": "XLUNLITURBOHSTANDARD7H_P", "package_id": "VWM1ZWF0Nk1GQW9MRTEyajJnWFcrdw",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Premium - Pulsa",
        "package_code": "XLUNLITURBOHPREMIUM7H_P", "package_id": "N3IvV0NHUEtNUzV6ZlNYR0l0MTNuUQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Super - Pulsa",
        "package_code": "XLUNLITURBOHSUPER7H_P", "package_id": "cldEcVNPYytBQTUzbm02QTJ4YmdaQQ",
        "harga": "Rp. 5", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Basic - Dana/QRIS",
        "package_code": "XLUNLITURBOHBASIC7H", "package_id": "Y1VHUkhld0dZUUluT0d0VkJHdUp5QQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Standard - Dana/QRIS",
        "package_code": "XLUNLITURBOHSTANDARD7H", "package_id": "d1FUOWdCdklQcVVpeWtrajduWmRZUQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Super - Dana/QRIS",
        "package_code": "XLUNLITURBOHSUPER7H", "package_id": "MCtPK1g3dG1uRS9tNDhxQlIwSnJSUQ",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
    {
        "package_name_show": "V3 Unlimited Turbo Premium - Qris/Dana",
        "package_code": "XLUNLITURBOHPREMIUM7H", "package_id": "UFJLOTl6TkNiT3poY2VYd2tTbStldw",
        "harga": "Rp. 0", "jenis": "otp", "category": "addon"
    },
]

async def handle_pricelist_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Router untuk semua callback query yang berhubungan dengan pricelist."""
    query = update.callback_query
    command = query.data
    
    if command == "buy_package_menu":
        await buy_package_menu(update, context)
    elif command.startswith("category_"):
        category = command.split('category_')[-1]
        await show_category_products(update, context, category)
    elif command.startswith("show_product_"):
        package_code = command.split('show_product_')[-1]
        await show_product_details(update, context, package_code)
    elif command.startswith("lihat_semua_paket_"):
        page_index = int(command.split('_')[-1])
        await lihat_semua_paket(update, context, page_index)
    else:
        await query.edit_message_text(f"Perintah pricelist tidak dikenal: {command}")


async def buy_package_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Menampilkan menu kategori pembelian."""
    query = update.callback_query
    await query.edit_message_text(
        "Silakan pilih kategori paket yang ingin Anda beli:",
        reply_markup=BUY_MENU_KEYBOARD
    )


async def show_category_products(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
    """Menampilkan daftar produk berdasarkan kategori yang dipilih."""
    query = update.callback_query
    keyboard = create_product_list_keyboard(MY_PRODUCT_LIST, category)
    await query.edit_message_text(
        f"Berikut adalah daftar paket untuk kategori *{category.upper()}*:",
        parse_mode='Markdown',
        reply_markup=keyboard
    )
    
async def show_product_details(update: Update, context: ContextTypes.DEFAULT_TYPE, package_code: str) -> None:
    """Mengambil detail paket dari API dan menampilkannya."""
    query = update.callback_query
    await query.edit_message_text("Sedang mengambil detail paket...")

    try:
        product_info = next((p for p in MY_PRODUCT_LIST if p['package_code'] == package_code), None)
        if not product_info:
            await query.edit_message_text("Produk tidak ditemukan.", reply_markup=BACK_BUTTON_TO_MAIN)
            return

        jenis_paket = product_info['jenis']
        url = f"{config.API_BASE_URL}list_paket?hesdastore={config.HESDASTORE_KEY}&jenis={jenis_paket}"
        response = requests.get(url, auth=(config.EMAIL_ANDA, config.PASSWORD_ANDA))
        response.raise_for_status()
        data = response.json()
        
        if data['status'] and data['data']:
            product_detail = next((item for item in data['data'] if item['package_code'] == package_code), None)
            if product_detail:
                package_name = product_detail.get('package_name_show', 'N/A')
                harga = product_detail.get('harga', 'N/A')
                deskripsi = product_detail.get('package_description_show', 'Tidak ada deskripsi.')
                deskripsi = deskripsi.replace('\\r\\n', '\n').replace('•', '-')
                message = (
                    f"**Detail Paket:**\n\n"
                    f"📦 *{package_name}*\n"
                    f"💰 Harga: {harga}\n"
                    f"ℹ️ Deskripsi:\n{deskripsi}\n"
                    f"----------------------------------------\n"
                )
                message = message.replace('<b>', '*').replace('</b>', '*')
                await query.edit_message_text(
                    message,
                    parse_mode='Markdown',
                    reply_markup=BACK_BUTTON_TO_BUY_MENU
                )
            else:
                await query.edit_message_text("Detail produk tidak ditemukan.", reply_markup=BACK_BUTTON_TO_MAIN)
        else:
            await query.edit_message_text(
                f"Tidak ada paket tersedia untuk jenis {jenis_paket}.",
                reply_markup=BACK_BUTTON_TO_MAIN
            )
    except Exception as e:
        logger.error(f"Terjadi kesalahan di show_product_details: {e}")
        await query.edit_message_text("Terjadi kesalahan tak terduga. Hubungi admin.", reply_markup=BACK_BUTTON_TO_MAIN)

async def lihat_semua_paket(update: Update, context: ContextTypes.DEFAULT_TYPE, page_index: int = 0) -> None:
    """Fungsi debug untuk melihat semua produk dari API dengan pagination."""
    query = update.callback_query
    
    if 'all_packages' not in context.user_data or page_index == 0:
        await query.edit_message_text("Sedang mengambil semua daftar paket dari API...")
        try:
            all_packages = []
            for jenis in ["nonotp", "otp", "unreg"]:
                url = f"{config.API_BASE_URL}list_paket?hesdastore={config.HESDASTORE_KEY}&jenis={jenis}"
                response = requests.get(url, auth=(config.EMAIL_ANDA, config.PASSWORD_ANDA))
                response.raise_for_status()
                data = response.json()
                if data['status'] and data['data']:
                    all_packages.extend(data['data'])
            context.user_data['all_packages'] = all_packages
        except Exception as e:
            await query.edit_message_text(f"Terjadi kesalahan saat mengambil data: {e}", reply_markup=BACK_BUTTON_TO_MAIN)
            return
    
    all_packages = context.user_data.get('all_packages', [])
    items_per_page = 5
    total_items = len(all_packages)
    total_pages = math.ceil(total_items / items_per_page)
    
    start_index = page_index * items_per_page
    end_index = start_index + items_per_page
    paginated_items = all_packages[start_index:end_index]
    
    if not paginated_items:
        await query.edit_message_text("Tidak ada paket yang ditemukan dari API.", reply_markup=BACK_BUTTON_TO_MAIN)
        return

    message = f"**Semua Paket dari API** (Hal. {page_index + 1}/{total_pages})\n\n"
    for item in paginated_items:
        message += f"📦 *{item.get('package_name_show', 'N/A')}*\n"
        message += f"🔑 `package_code`: `{item.get('package_code', 'N/A')}`\n"
        message += f"🆔 `package_id`: `{item.get('package_id', 'N/A')}`\n"
        message += f"💰 Harga: {item.get('harga', 'N/A')}\n"
        message += f"🔗 Jenis: `{item.get('jenis', 'N/A')}`\n"
        message += "----------------------------------------\n"
    
    await query.edit_message_text(
        message,
        parse_mode='Markdown',
        reply_markup=create_pagination_keyboard(page_index, total_pages, "lihat_semua_paket")
    )