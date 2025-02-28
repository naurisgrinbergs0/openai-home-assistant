from telegram import Update
from telegram_api import configuration, recipients
from utility import config


async def handle_command(update: Update, _):
    command_name = update.message.text[1:]
    if command_name == configuration.subscribe_command_name:
        await handle_subscribe_command(update)
    elif command_name == configuration.unsubscribe_command_name:
        await handle_unsubscribe_command(update)


# Adds user to recipient list
async def handle_subscribe_command(update: Update, _):
    list_of_recipients = config.retrieve_config("telegram_recipients")
    recipient = recipients.find_recipient(update.message.chat_id)

    if not list_of_recipients:
        list_of_recipients = []

    if not recipient:
        list_of_recipients.append(
            {
                "chat_id": update.message.chat_id,
                "name": update.message.chat.first_name,
            }
        )
        config.store_config("telegram_recipients", list_of_recipients)
        await update.message.reply_text(configuration.subscribed_successfully_message)
    else:
        await update.message.reply_text(configuration.subscribed_already_message)


# Removes user from recipient list
async def handle_unsubscribe_command(update: Update, _):
    list_of_recipients = config.retrieve_config("telegram_recipients")
    recipient = recipients.find_recipient(update.message.chat_id)

    if recipient:
        list_of_recipients.remove(recipient)
        config.store_config("telegram_recipients", list_of_recipients)
        await update.message.reply_text(configuration.unsubscribed_successfully_message)
    else:
        await update.message.reply_text(configuration.unsubscribed_already_message)
