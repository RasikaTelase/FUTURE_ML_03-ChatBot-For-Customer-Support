
import streamlit as st
from bot_logic import SimpleChatBot
from datetime import datetime
import time
import threading
import asyncio
from datetime import datetime
import openai

openai.api_key = "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"

def general_fallback(user_input):
    user_input = user_input.lower()

    if "date" in user_input:
        today = datetime.now().strftime("%Y-%m-%d")
        return f"📅 Today’s date is {today}"
    elif "day" in user_input:
        today = datetime.now().strftime("%A")
        return f"📆 Today is {today}"
    elif "time" in user_input:
        now = datetime.now().strftime("%H:%M:%S")
        return f"⏰ Current time is {now}"
    else:
        return None
    
def gpt_fallback(user_input):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_input}]
    )
    return response.choices[0].message.content


# -------------------------------
# TELEGRAM BOT SETUP
# -------------------------------
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

bot_logic = SimpleChatBot()  # Shared bot instance

TELEGRAM_TOKEN = "8400496735:AAE0gKpAM_r53wHZ0nNIC3n_NBrPTNV4rIU"

async def tg_start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Hello! I am your Smart Support Bot.")

async def tg_handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = bot_logic.get_response(user_message)
    await update.message.reply_text(f"🤖 {response}")

def run_telegram_bot(token):
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", tg_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, tg_handle_message))
    print("🤖 Telegram bot is running...")
    app.run_polling()

def start_telegram_bot_in_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    run_telegram_bot(TELEGRAM_TOKEN)

# Start Telegram bot in background thread
threading.Thread(target=start_telegram_bot_in_thread, daemon=True).start()

# -------------------------------
# STREAMLIT CHATBOT
# -------------------------------
# Initialize Streamlit session state
if 'bot' not in st.session_state:
    st.session_state.bot = bot_logic
    st.session_state.history = []
    st.session_state.proactive_sent = False

# Header
st.markdown(
    "<h1 style='text-align:center; color:white; background-color:#4B0082; padding:12px; border-radius:12px;'>"
    "🤖 Smart Customer Support Chatbot</h1>", unsafe_allow_html=True
)
st.markdown("<p style='text-align:center; color:#FFFFFF;'>Handle real-time customer queries efficiently using AI + FAQs!</p>",
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Options")
    if st.button("🗑️ Reset Chat"):
        st.session_state.history = []
    if st.button("📞 Connect to Human Agent"):
        st.session_state.history.append(("Bot", "🔹 You are now connected to a human agent."))
    with st.expander("ℹ️ About Bot"):
        st.write("""
        This chatbot handles customer queries using:
        - Predefined FAQ matching
        - AI fallback (OpenAI GPT)
        - Quick reply options
        - Rich media support
        """)

# Proactive message
if not st.session_state.proactive_sent:
    st.session_state.history.append(("Bot", "🤖 Hello! How can I assist you today?"))
    st.session_state.proactive_sent = True

# FAQ buttons
faq_questions = [
    "What are your working hours?",
    "How can I reset my password?",
    "Where can I track my order?",
    "What is the return policy?"
]
st.markdown("### ❓ Quick Questions")
cols = st.columns(len(faq_questions))
for i, question in enumerate(faq_questions):
    if cols[i].button(question):
        user_input = question
        st.session_state.history.append(("You", f"💬 {user_input}"))
        response = bot_logic.get_response(user_input)
        st.session_state.history.append(("Bot", f"🤖 {response}"))

# User input
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your message here...", "")
    submit_button = st.form_submit_button(label="Send")
if submit_button and user_input:
    st.session_state.history.append(("You", f"💬 {user_input}"))
    response = bot_logic.get_response(user_input)
    st.session_state.history.append(("Bot", f"🤖 {response}"))

# Display chat history
for sender, msg in st.session_state.history:
    timestamp = datetime.now().strftime("%H:%M")
    if sender == "You":
        st.chat_message("user").write(f"<span style='color:#1E90FF;'>{msg} ⏰ {timestamp}</span>",
                                     unsafe_allow_html=True)
    else:
        chat_msg = st.chat_message("assistant")
        chat_msg.write(f"<span style='color:#32CD32;'>{msg} ⏰ {timestamp}</span>", unsafe_allow_html=True)

        # Rich media example
        if "track order" in msg.lower():
            chat_msg.image("https://via.placeholder.com/250x150.png?text=Order+Tracking+Image", caption="Your Order Status")
            if chat_msg.button("🔗 Track Now"):
                st.session_state.history.append(("Bot", "🔹 Redirecting you to the tracking page..."))

        # Feedback buttons with unique keys
        import uuid
        col1, col2 = st.columns([0.1, 0.1])
        with col1:
            if st.button("👍", key=f"like_{uuid.uuid4()}"):
                st.success("Thanks for your feedback!")
        with col2:
            if st.button("👎", key=f"dislike_{uuid.uuid4()}"):
                st.warning("We will try to improve!")
async def tg_handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = bot_logic.get_response(user_message)
    
    await update.message.reply_text(f"🤖 {response}")
    
    # Send an image if needed
    if "track order" in user_message.lower():
        await update.message.reply_photo(
            photo="https://via.placeholder.com/250.png",
            caption="📦 Your Order Status"
        )
async def tg_handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = bot_logic.get_response(user_message)
    
    # 1️⃣ Send bot's text response
    await update.message.reply_text(f"🤖 {response}")

    # 2️⃣ Check for specific keywords to send images or rich media
    if "track order" in user_message.lower():
        # Send an image along with caption
        await update.message.reply_photo(
            photo="https://via.placeholder.com/250.png",
            caption="📦 Your Order Status"
        )
    elif "return policy" in user_message.lower():
        await update.message.reply_text(
            "🔄 Our return policy allows returns within 30 days from purchase."
        )
    elif "working hours" in user_message.lower():
        await update.message.reply_text(
            "🕒 Our working hours are 9 AM - 6 PM, Monday to Friday."
        )
    elif "reset password" in user_message.lower():
        await update.message.reply_text(
            "🔑 You can reset your password here: https://example.com/reset"
        )

