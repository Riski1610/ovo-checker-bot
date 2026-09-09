import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from services.ovo_checker import OVOChecker
import re

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize OVO Checker
ovo_checker = OVOChecker()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN not found in .env file")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    welcome_text = (
        "👋 Selamat datang di OVO Checker Bot!\n\n"
        "Bot ini membantu Anda mengecek apakah nomor HP terdaftar di OVO atau belum.\n\n"
        "Cara penggunaan:\n"
        "📱 Kirim nomor HP (contoh: 081234567890)\n\n"
        "Perintah:\n"
        "/start - Tampilkan menu ini\n"
        "/help - Bantuan\n"
        "/about - Tentang bot"
    )
    await update.message.reply_text(welcome_text)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    help_text = (
        "📖 <b>Bantuan</b>\n\n"
        "1. Kirim nomor HP yang ingin dicek\n"
        "2. Bot akan memproses dan memberikan hasil\n"
        "3. Hasil: ✅ Terdaftar atau ❌ Belum Terdaftar\n\n"
        "<b>Format nomor:</b>\n"
        "- 08xxxxxxxxxx (format Indonesia)\n"
        "- +628xxxxxxxxxx (dengan kode negara)"
    )
    await update.message.reply_text(help_text, parse_mode='HTML')


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /about is issued."""
    about_text = (
        "ℹ️ <b>Tentang Bot</b>\n\n"
        "OVO Checker Bot v1.0\n"
        "Dibuat untuk mengecek status registrasi nomor OVO\n\n"
        "⚠️ Disclaimer:\n"
        "Bot ini hanya untuk keperluan verifikasi nomor OVO secara umum."
    )
    await update.message.reply_text(about_text, parse_mode='HTML')


def is_phone_number(text: str) -> bool:
    """Validate if text is a valid phone number."""
    # Remove spaces
    text = text.replace(' ', '')
    # Check if it matches phone number pattern
    phone_regex = r'^(\+62|62|0)[0-9]{9,12}$'
    return bool(re.match(phone_regex, text))


def normalize_phone_number(phone: str) -> str:
    """Normalize phone number to standard format (08xxx)."""
    # Remove spaces
    phone = phone.replace(' ', '')
    
    # Convert to 0 prefix format
    if phone.startswith('+62'):
        return '0' + phone[3:]
    elif phone.startswith('62'):
        return '0' + phone[2:]
    
    return phone


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages (phone numbers)."""
    user_input = update.message.text.strip()
    
    # Validate phone number format
    if not is_phone_number(user_input):
        await update.message.reply_text(
            "❌ Format nomor tidak valid. Silakan kirim nomor HP yang benar (contoh: 081234567890)"
        )
        return
    
    try:
        # Show typing indicator
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # Normalize phone number
        phone_number = normalize_phone_number(user_input)
        
        # Show loading message
        loading_msg = await update.message.reply_text("⏳ Sedang mengecek...")
        
        # Check OVO registration status
        result = await ovo_checker.check_ovo_registration(phone_number)
        
        # Delete loading message
        await loading_msg.delete()
        
        # Send result
        if result['success']:
            status_emoji = "✅" if result['isRegistered'] else "❌"
            status_text = "TERDAFTAR" if result['isRegistered'] else "BELUM TERDAFTAR"
            
            from datetime import datetime
            current_time = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
            
            result_text = (
                f"{status_emoji} <b>Hasil Pengecekan</b>\n\n"
                f"📱 Nomor: {result['phoneNumber']}\n"
                f"📊 Status: {status_text}\n"
                f"⏰ Waktu: {current_time}"
            )
            
            await update.message.reply_text(result_text, parse_mode='HTML')
        else:
            await update.message.reply_text(f"❌ Error: {result['message']}")
    
    except Exception as error:
        logger.error(f"Error: {error}")
        await update.message.reply_text("❌ Terjadi kesalahan. Silakan coba lagi nanti.")


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a message to notify the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    await update.message.reply_text("❌ Terjadi kesalahan pada bot.")


def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about_command))
    
    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # log all errors
    application.add_error_handler(error_handler)
    
    # Run the bot
    print("🤖 OVO Checker Bot is running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
