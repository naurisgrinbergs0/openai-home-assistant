from telegram import Update
from telegram_api.connection import app


async def handle_text_message(update: Update, _):
    print("MESSAGE RECEIVED")


async def send_image(chats, photo, caption):
    if not chats:
        return
    for chat in chats:
        await app.bot.send_photo(chat["chat_id"], photo=photo, caption=caption)


async def send_message(chats, text):
    if not chats:
        return
    for chat in chats:
        await app.bot.send_message(chat["chat_id"], text=text)
