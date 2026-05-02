import logging
import json
import os
from datetime import date
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ---- SETTINGS ----
TOKEN = os.environ.get("BOT_TOKEN", "PASTE_YOUR_BOT_TOKEN_HERE")

# ---- SETUP ----
logging.basicConfig(level=logging.INFO)
DATA_FILE = "streak_data.json"

# ---- MEMORY ----
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"streak": 0, "last_date": None}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# ---- COMMANDS ----
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Your Chat ID is: {update.message.chat_id}")
    await update.message.reply_text(
        "Hi! I am your Writing Streak Bot 🔥\n\nType /check to log whether you wrote today."
    )

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Yes ✅", "No ❌"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    await update.message.reply_text("Did you write today?", reply_markup=reply_markup)

async def handle_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = load_data()
    text = update.message.text.lower()
    today = str(date.today())

    if "yes" in text:
        if data["last_date"] == today:
            await update.message.reply_text("Already logged today! Keep it up 🔥")
            return
        data["streak"] += 1
        data["last_date"] = today
        save_data(data)
        await update.message.reply_text(
            f"Amazing! 🔥 You are on a {data['streak']} day streak! Keep writing!"
        )
    elif "no" in text:
        data["streak"] = 0
        data["last_date"] = today
        save_data(data)
        await update.message.reply_text(
            "No worries. Tomorrow is a new day. Streak reset — come back stronger 💪"
        )

# ---- RUN ----
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_response))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
