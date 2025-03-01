
import settings as s
import websocket
import json
from openai_api import configuration
import utility.config as config
import utility.file as file

def on_message(ws, message):
    data = json.loads(message)

    match data["type"]:
        case "response.audio_transcript.done":
            print("| Output: ", data["transcript"])
        case "conversation.item.input_audio_transcription.completed":
            print("| Input: ", data["transcript"])
        case ("session.created" | "session.updated" | "response.audio.delta" | "response.audio_transcript.delta" | "rate_limits.updated"
              | "response.audio.done" | "conversation.item.created" | "response.content_part.done" | "response.output_item.done"
              | "response.done" | "response.content_part.added" | "response.output_item.added" | "response.created"
              | "input_audio_buffer.committed" | "input_audio_buffer.speech_started"):
            # print("EVENT: ", data["type"])
            pass
        case _:
            print(json.dumps(data, indent=2))


def update_session(ws):
    session_update = {
        "type": "session.update",
        "session": {
            "modalities": ["text", "audio"],
            # "model": "gpt-4o-realtime-preview",
            "instructions": configuration.assistant_instructions,
            # "voice": "alloy",
            # "turn_detection": {"type": "server_vad", "threshold": 0.3, "prefix_padding_ms": 300, "silence_duration_ms": 200},
            # "input_audio_format": "pcm16",
            # "output_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": "whisper-1",
                "language": "lv",
                "prompt": "Latviešu valoda",
            },
            "tool_choice": "auto",
            # "temperature": 0.8,
            # "max_response_output_tokens": "inf",
            # "tools": []
        }
    }
    ws.send(json.dumps(session_update))

def send_message(ws):
    update_session(ws)

    audioBase64 = file.base64_encode_audio(config.get_data_file_path("RECORDING_FILE_NAME"))

    # Useful for adding convo items
    # event = {
    #     "type": "conversation.item.create",
    #     "item": {
    #         "type": "message",
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "input_audio",
    #                 "audio": audioBase64,
    #             }
    #         ],
    #     },
    # }

    event = {
        "type": "input_audio_buffer.append",
        "audio": audioBase64,
    }
    ws.send(json.dumps(event))
    event = {
        "type": "input_audio_buffer.commit",
    }
    ws.send(json.dumps(event))

    event = {
        "type": "response.create",
        "response": {
            "modalities": [ "text", "audio" ],
        }
    }
    ws.send(json.dumps(event))