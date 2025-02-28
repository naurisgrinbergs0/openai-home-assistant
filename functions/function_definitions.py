import settings as s
import os
from utility import config

# Template to use for functions that have no params
params_empty = {
    "type": "object",
    "properties": {},
    "required": [],
}

# Placeholders
placeholder_all = "<all>"


# Sets / Updates function definition array
def get_function_definitions():
    global function_definitions
    function_definitions = [
        {
            "type": "function",
            "function": {
                "name": s.functions["TOGGLE_LIGHTS"],
                "description": "Toggles lights",
                "parameters": params_empty,
            },
        },
        {
            "type": "function",
            "function": {
                "name": s.functions["TAKE_PICTURE"],
                "description": "Takes a photo. Gives assistant ability to see. Gives assistant info about environment. Gives insight about what user shows",
                "parameters": params_empty,
            },
        },
        {
            "type": "function",
            "function": {
                "name": s.functions["GET_WEATHER"],
                "description": "Retrieves weather, forecast, historical weather, sunrise/sunset, moonphase info",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": f"Location (Only if user gave specific location, otherwise use: {os.getenv('LOCATION')})",
                        },
                        "date": {
                            "type": "string",
                            "description": "Date (yyyy-MM-dd)",
                        },
                        "time": {
                            "type": "string",
                            "description": "Time (hh:00:00)",
                        },
                        "post_action_send_telegram_message": get_post_action_send_telegram_message(),
                    },
                    "required": [],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": s.functions["GENERATE_IMAGE"],
                "description": "Generates image or variation of existing image using a prompt text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "prompt": {
                            "type": "string",
                            "description": "Prompt text",
                        },
                        "image_source_for_variation": {
                            "type": "string",
                            "enum": ["camera", "previous_image"],
                            "description": "Source for image variation generation",
                        },
                        "post_action_send_telegram_message": get_post_action_send_telegram_message(),
                    },
                    "required": ["prompt"],
                },
            },
        },
    ]
    return function_definitions


def get_post_action_send_telegram_message():
    telegram_recipients = config.retrieve_config("telegram_recipients")
    if not telegram_recipients:
        telegram_recipients = []

    telegram_recipient_options = [placeholder_all] + [
        f"{sub['name']}:{sub['chat_id']}" for sub in telegram_recipients
    ]

    return {
        "type": "object",
        "description": "Post action - send telegram message",
        "properties": {
            "recipients": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": telegram_recipient_options,
                },
            },
        },
    }
