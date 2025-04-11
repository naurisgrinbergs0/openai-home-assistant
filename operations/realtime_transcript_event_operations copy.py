import os
import time
import json
import settings as s
from interface.web_socket import WebSocketInterface
from interface.audio_player import AudioPlayer
from openai_api import configuration
from utility import convert
from functions import function_definitions, function_processing


def get_headers():
    return [
        "Authorization: Bearer " + os.getenv("OPENAI_API_KEY"),
        "OpenAI-Beta: realtime=v1",
    ]

already_received = False
def on_message(message, ws_interface: WebSocketInterface, audio_player: AudioPlayer, send_time):
    if message.strip():
        data = json.loads(message)

    match data["type"]:
        case "response.audio.delta":
            global already_received
            # audio_player.append_audio_chunks(convert.base64_to_bytes(data["delta"]))
            if not already_received:
                already_received = True
            pass
        case "response.done":
            if data["response"]["output"] and data["response"]["output"][0]["type"] == "function_call":
                results = function_processing.process_function_calls(data["response"]["output"])
                for result in results:
                    send_function_call_result(ws_interface, result)
                request_response(ws_interface)
            # elif data["response"]["status_details"]["error"]["type"] == "insufficient_quota":
            #     print("INSUFFICIENT QUOTA")
        case "response.audio.done":
            #     audio_player.stop_playing()
            pass
        case "session.updated":
            #     print(json.dumps(data, indent=2))
            pass
        case "response.audio_transcript.done":
            print("| Output: ", data["transcript"])
        case "conversation.item.input_audio_transcription.completed":
            print("| Input: ", data["transcript"])
        case (
            "session.created" | "response.audio_transcript.delta" | "rate_limits.updated" |
            "conversation.item.created" | "response.content_part.done" | "response.output_item.done" |
            "response.function_call_arguments.done" | "response.function_call_arguments.delta" |
            "response.content_part.added" | "response.output_item.added" | "response.created" |
            "input_audio_buffer.committed" | "input_audio_buffer.speech_started"):
            # print("EVENT: ", data["type"])
            pass
        case _:
            print(json.dumps(data, indent=2))


def update_session(ws_interface: WebSocketInterface):
    event = {
        "type": "session.update",
        "session":
            {
                "modalities": ["text", "audio"],
                # "model": "gpt-4o-realtime-preview",
                "instructions": configuration.assistant_instructions,
                "voice": "ballad",
                "turn_detection": None,
                # "turn_detection": {"type": "server_vad", "threshold": 0.3, "prefix_padding_ms": 300, "silence_duration_ms": 200},
                # "input_audio_format": "pcm16",
                # "output_audio_format": "pcm16",
                "input_audio_transcription":
                    {
                        "model": "whisper-1",
                        "language": s.locale["LANGUAGE_CODE"],
                        # "prompt": "Latviešu valoda",
                    },
                "tool_choice": "auto",
                "temperature": 0.8,
                "max_response_output_tokens": 4096,
                "tools": function_definitions.get_function_definitions()
            }
    }
    ws_interface.send_message(json.dumps(event))


def send_audio_chunk(ws_interface: WebSocketInterface, audio_chunk):
    audio_chunk_base64 = convert.bytes_to_base64(audio_chunk)
    event = {
        "type": "input_audio_buffer.append",
        "audio": audio_chunk_base64,
    }
    ws_interface.send_message(json.dumps(event))


def commit_audio_chunks(ws_interface: WebSocketInterface):
    event = {
        "type": "input_audio_buffer.commit",
    }
    ws_interface.send_message(json.dumps(event))


def clear_audio_buffer(ws_interface: WebSocketInterface):
    event = {
        "type": "input_audio_buffer.clear",
        "type": "conversation.item.truncate",
    }
    ws_interface.send_message(json.dumps(event))


def insert_conversation_item(ws_interface: WebSocketInterface, role, text=None, audio_bytes=None):
    content = {
        "type": "input_text" if text else "input_audio",
    }
    if text:
        content["text"] = text
    else:
        audio_base64 = convert.bytes_to_base64(audio_bytes)
        content["audio"] = audio_base64
        
    event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": role,
            "content": [content]
        }
    }
    ws_interface.send_message(json.dumps(event))


def send_function_call_result(ws_interface: WebSocketInterface, result):
    event = {
        "type": "conversation.item.create",
        "item":
            {
                "type": "function_call_output",
                "call_id": result["call_id"],
                "output": f"Error: {result["error"]}" if result["error"] else result["result"]
            }
    }
    ws_interface.send_message(json.dumps(event))


def request_response(ws_interface: WebSocketInterface):
    event = {"type": "response.create", "response": {"modalities": ["text", "audio"],}}
    ws_interface.send_message(json.dumps(event))
