from functions.function_definitions import get_function_definitions
from openai_api.connection import client
import settings as s


def generate_completion(messages):
    response_stream = client.chat.completions.create(
        model=s.openai["COMPLETIONS_MODEL"],
        tools=get_function_definitions(),
        messages=messages,
        max_tokens=s.openai["CONVERSATION_RESPONSE_MAX_TOKEN_COUNT"],
        stream=True,
    )

    return response_stream


def generate_vision_completion(messages, capture_base64):
    response_stream = client.chat.completions.create(
        model=s.openai["VISION_MODEL"],
        max_tokens=s.openai["CONVERSATION_RESPONSE_MAX_TOKEN_COUNT"],
        stream=True,
        messages=messages
        + [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": messages[-1]["content"]},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{capture_base64}"
                        },
                    },
                ],
            }
        ],
    )

    return response_stream
