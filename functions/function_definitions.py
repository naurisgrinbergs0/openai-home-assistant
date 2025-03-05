import settings as s

# Templates
params_empty = {
    "type": "object",
    "properties": {},
    "required": [],
}

# Function definitions
get_weather = {
    "type": "function",
    "name": s.functions["GET_WEATHER"],
    "description": "Retrieves weather, forecast, historical weather, sunrise/sunset, moonphase info",
    "parameters":
        {
            "type": "object",
            "properties":
                {
                    "location": {
                        "type": ["string", "null"],
                        "description": "Location (can be empty)",
                    },
                    "date": {
                        "type": ["string", "null"],
                        "description": "Date (yyyy-MM-dd)",
                    },
                    "time": {
                        "type": ["string", "null"],
                        "description": "Time (hh:00:00)",
                    },
                },
            "required": [],
        },
}

take_picture = {
    "type":
        "function",
    "name":
        s.functions["TAKE_PICTURE"],
    "description":
        "Takes a photo. Gives assistant ability to see. Gives assistant info about it's environment. Gives insight about what user sees",
    "parameters":
        {
            "type": "object",
            "properties":
                {
                    "prompt": {
                        "type": ["string", "null"],
                        "description": "Question or prompt about the photo",
                    },
                },
            "required": [],
        },
}

toggle_lights = {
    "type": "function",
    "name": s.functions["TOGGLE_LIGHTS"],
    "description": "Toggles lights",
    "parameters": params_empty,
}

telegram_send_message = {
    "type": "function",
    "name": s.functions["TELEGRAM_SEND_MESSAGE"],
    "description": "Sends message to user via Telegram",
    "parameters":
        {
            "type": "object",
            "properties":
                {
                    "recipient":
                        {
                            "type": "string",
                            "enum": ["all"],  # TODO: add recipients from file
                            "description": "Recipient of message",
                        },
                    "message": {
                        "type": "string",
                        "description": "Message to send",
                    },
                },
            "required": ["message"],
        },
}

telegram_send_picture = {
    "type":
        "function",
    "name":
        s.functions["TELEGRAM_SEND_PICTURE"],
    "description":
        "Sends image to user via Telegram. Image can be generated using prompt/taken by camera or last generated/taken image can be used",
    "parameters":
        {
            "type": "object",
            "properties":
                {
                    "recipient":
                        {
                            "type": "string",
                            "enum": ["all"],  # TODO: add recipients from file
                            "description": "Recipient of message",
                        },
                    "source":
                        {
                            "type": "string",
                            "enum": ["generate", "capture", "recent_image"],
                            "description": "Prompt text",
                        },
                    "prompt": {
                        "type": "string",
                        "description": "Text prompt for generating image",
                    },
                    # "image_source_for_variation":
                    #     {
                    #         "type": "string",
                    #         "enum": ["camera", "previous_image"],
                    #         "description": "Source for image variation generation",
                    #     },
                },
            "required": ["source"],
        },
}

get_user_input = {
    "type":
        "function",
    "name":
        s.functions["GET_USER_INPUT"],
    "description":
        "Allows user to answer assistant's question or say something to assistant. Always call this if input is expected from user",
    "parameters":
        params_empty,
}


# Retrieves function definition array
def get_function_definitions():
    function_definitions = [
        get_weather, take_picture, toggle_lights, telegram_send_message, telegram_send_picture, get_user_input
    ]
    return function_definitions


# placeholder_all = "<all>"
# def get_post_action_send_telegram_message():
#     telegram_recipients = config.retrieve_config("telegram_recipients")
#     if not telegram_recipients:
#         telegram_recipients = []

#     telegram_recipient_options = [placeholder_all] + [f"{sub['name']}:{sub['chat_id']}" for sub in telegram_recipients]

#     return {
#         "type": "object",
#         "description": "Post action - send telegram message",
#         "properties":
#             {
#                 "recipients": {
#                     "type": "array",
#                     "items": {
#                         "type": "string",
#                         "enum": telegram_recipient_options,
#                     },
#                 },
#             },
#     }
