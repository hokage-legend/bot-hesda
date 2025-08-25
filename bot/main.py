import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

import config
from handlers import start, handle_callback_query

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

def main() -> None:
    """Fungsi utama untuk menjalankan bot."""
    application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    
    # Handler utama untuk semua tombol inline
    application.add_handler(CallbackQueryHandler(handle_callback_query))
    
    print("Bot berhasil dijalankan...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()