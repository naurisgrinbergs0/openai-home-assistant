from openai_api import completions
from openai_api import configuration
from utility import datetime
import settings as s
import json
from response.function_processing import process_function_calls

system_instructions_messages = []
messages = []

# TODO: check if response to a tool call is successful


# Function to process the text stream and populate the array
def parallel_phrase_generation(
    phrase_queue, prompt, capture_base64, tool_call_id_replying_to
):
    phrase_end_chars = [".", "!", "?", ":", ";"]
    phrase_force_end_chars = [" ", ".", ",", "!", "?", ":", ";", "-", "/"]
    full_response_text = ""
    phrase = ""
    func_calls = []
    response_stream = None

    process_system_instructions_messages()
    process_messages()

    # Start generating
    if capture_base64:
        messages.append({"role": "user", "content": prompt})
        response_stream = completions.generate_vision_completion(
            system_instructions_messages + messages, capture_base64
        )
    else:
        if tool_call_id_replying_to:
            messages.append(
                {
                    "role": "tool",
                    "content": prompt,
                    "tool_call_id": tool_call_id_replying_to,
                }
            )
        messages.append({"role": "user", "content": prompt})
        response_stream = completions.generate_completion(
            system_instructions_messages + messages
        )

    # Process stream
    for chunk in response_stream:
        content = chunk.choices[0].delta.content
        tool_calls = chunk.choices[0].delta.tool_calls

        if content:
            # End and queue the phrase (if too long - force end)
            if (len(phrase) > 50 and content[0] in phrase_end_chars) or (
                len(phrase) > 500 and content[0] in phrase_force_end_chars
            ):
                phrase_queue.put(phrase)
                phrase = ""
            phrase += content
            full_response_text += content

        # Looks like API doesn't support multiple simulltaneous tool calls right now - only 1 will be added
        elif tool_calls:
            if len(func_calls) == 0:
                func_calls.append({})
            tool_call = tool_calls[0].function
            if tool_calls[0].id:
                func_calls[0]["id"] = tool_calls[0].id
            if tool_call.name:
                func_calls[0]["name"] = tool_call.name
            if tool_call.arguments:
                if (
                    func_calls[0].get("arguments")
                    or func_calls[0].get("arguments") == ""
                ):
                    func_calls[0]["arguments"] += tool_call.arguments
                else:
                    func_calls[0]["arguments"] = tool_call.arguments

    if phrase != "":
        phrase_queue.put(phrase)
    phrase_queue.put(None)  # Signal the end of the phrases

    # Add message to context
    if full_response_text != "":
        messages.append({"role": "assistant", "content": full_response_text})

    # Process function calls
    process_function_calls(func_calls, prompt)


def process_system_instructions_messages():
    global system_instructions_messages
    system_instructions_messages = [
        {
            "role": "system",
            "content": configuration.assistant_instructions,
        },
        {
            "role": "system",
            "content": f"current_time_settings: {json.dumps(datetime.get_current_time_settings())}",
        },
    ]


def process_messages():
    if len(messages) >= s.openai["CONVERSATION_CONTEXT_MESSAGE_COUNT"]:
        messages.pop(0)
