import asyncio
import os
from telegram import Bot

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

async def send_reminder():
    bot = Bot(token=TOKEN)
    await bot.send_message(
        chat_id=CHAT_ID,
        text="Hey Sean! 🖊️ Did you write today? Open your bot and type /check to log it and keep your streak alive 🔥"
    )

asyncio.run(send_reminder())
