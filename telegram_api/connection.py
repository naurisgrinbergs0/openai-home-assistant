from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    filters,
)
from telegram_api import configuration
import asyncio
import os
import threading

app = None
telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")


def init():
    global app

    app = Application.builder().token(telegram_token).build()

    add_command_handlers()
    add_message_handlers()
    add_error_handlers()

    if not telegram_token:
        return

    print("|-- Telegram bot initialized")


def start():
    if not telegram_token:
        return

    def start_loop(loop):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            app.run_polling(poll_interval=3, drop_pending_updates=True)
        )

    new_loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_loop, args=(new_loop,))
    t.start()


def handle_error():
    # TODO: log to file
    print("Telegram error")


def add_error_handlers():
    app.add_error_handler(handle_error)


def add_message_handlers():
    from telegram_api.messaging import handle_text_message

    app.add_handler(MessageHandler(filters.TEXT, handle_text_message))


def add_command_handlers():
    from telegram_api.commands import (
        handle_subscribe_command,
        handle_unsubscribe_command,
    )

    app.add_handler(
        CommandHandler(configuration.subscribe_command_name, handle_subscribe_command)
    )
    app.add_handler(
        CommandHandler(
            configuration.unsubscribe_command_name, handle_unsubscribe_command
        )
    )
