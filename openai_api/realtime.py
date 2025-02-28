import os
import settings as s
import websocket
import json
import utility.config as config
import utility.file as file

ws = None
headers = [
    "Authorization: Bearer " + os.getenv("OPENAI_API_KEY"),
    # "OpenAI-Beta: realtime=v1"
]

def _on_open(ws):
    print("Connected to server.")

def _on_message(ws, message):
    data = json.loads(message)

    # if data["type"] != "session.created":
    # print("Received event:", json.dumps(data, indent=2))

    if data["type"] == "response.done":
        print("RESPONSE: ", data["response"]["output"][0]["content"][0]["text"])

    # if data['type'] == "response.done":
    #     print("RESPONSE:", data['response']['output'][0]['content'][0]['text'])

    # if data.type == "response.done":
    #     print(data.response.output[0])

def init():
    global ws

    ws = websocket.WebSocketApp(
        s.openai["REALTIME_MODEL_URL"],
        header=headers,
        on_open=_on_open,
        on_message=_on_message,
    )
    print("|-- OpenAI realtime websocket connected")

def start():
    ws.run_forever()

def update_session():
    session_update = {
        "type": "session.update",
        "session": {
            # "modalities": ["text"],
            # "model": "gpt-4o-realtime-preview",
            "instructions": "Obligāti runā tikai latviešu valodā. Ar tevi runās tikai latviešu valodā.",
            "voice": "alloy",
            # "turn_detection": {"type": "server_vad", "threshold": 0.3, "prefix_padding_ms": 300, "silence_duration_ms": 200},
            # "input_audio_format": "pcm16",
            # "output_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": "whisper-1",
                "language": "lv",
                "prompt": "make text",
            },
            # "tool_choice": "auto",
            # "temperature": 0.8,
            # "max_response_output_tokens": "inf",
            # "tools": []
        }
    }
    ws.send(json.dumps(session_update))

def send_message():
    global ws

    update_session()

    # audioBase64 = file.base64_encode_audio(config.get_data_file_path("RECORDING_FILE_NAME"))
    audioBase64 = file.read_file_base64(config.get_data_file_path("RECORDING_FILE_NAME"))

    event = {
        "type": "conversation.item.create",
        "item": {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_audio",
                    "audio": audioBase64,
                }
            ],
        },
    }
    ws.send(json.dumps(event))

    event = {
        "type": "response.create",
        "response": {
            # "modalities": [ "text", "audio" ],
            "modalities": [ "text" ],
        }
    }
    ws.send(json.dumps(event))