import os
import json
import settings as s
from interface.web_socket import WebSocketInterface
from openai_api import configuration
from utility import convert


def get_headers():
    return [
        "Authorization: Bearer " + os.getenv("OPENAI_API_KEY"),
        "OpenAI-Beta: realtime=v1",
    ]


def on_message(message):
    data = json.loads(message)

    match data["type"]:
        case "response.audio_transcript.done":
            print("| Output: ", data["transcript"])
        case "conversation.item.input_audio_transcription.completed":
            print("| Input: ", data["transcript"])
        case (
            "session.created" | "session.updated" | "response.audio.delta" | "response.audio_transcript.delta" |
            "rate_limits.updated" | "response.audio.done" | "conversation.item.created" | "response.content_part.done" |
            "response.output_item.done" | "response.done" | "response.content_part.added" |
            "response.output_item.added" | "response.created" | "input_audio_buffer.committed" |
            "input_audio_buffer.speech_started"):
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
                # "voice": "alloy",
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
                # "temperature": 0.8,
                # "max_response_output_tokens": "inf",
                # "tools": []
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
    print("committttttt")
    event = {
        "type": "input_audio_buffer.commit",
    }
    ws_interface.send_message(json.dumps(event))


def request_response(ws_interface: WebSocketInterface):
    event = {"type": "response.create", "response": {"modalities": ["text", "audio"],}}
    ws_interface.send_message(json.dumps(event))
