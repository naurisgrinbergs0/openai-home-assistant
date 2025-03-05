from telegram_api import messaging, recipients


async def telegram_send_message(function_data):
    try:
        users = recipients.find_recipients(
            chat_ids=recipients.parse_recipient_array(function_data.arguments.get("recipient")))

        await messaging.send_message(users, function_data.arguments.get("message"))
    except Exception:
        return (None, "Unknown error")

    return ("success", None)
