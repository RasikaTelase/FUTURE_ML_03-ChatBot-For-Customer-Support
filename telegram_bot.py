import threading
import asyncio
from telegram_bot import run_telegram_bot  # your function

def start_bot_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    run_telegram_bot("8400496735:AAE0gKpAM_r53wHZ0nNIC3n_NBrPTNV4rIU")

threading.Thread(target=start_bot_in_thread, daemon=True).start()

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
from bot_logic import SimpleChatBot
import asyncio

bot_logic = SimpleChatBot()

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Hello! I am your Smart Support Bot.")

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = bot_logic.get_response(user_message)
    await update.message.reply_text(f"🤖 {response}")

app = ApplicationBuilder().token("8400496735:AAE0gKpAM_r53wHZ0nNIC3n_NBrPTNV4rIU").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Telegram bot is running...")
app.run_polling()
