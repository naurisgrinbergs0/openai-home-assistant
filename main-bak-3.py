import os
import settings as s
import websocket
import json
import utility.config as config
import utility.file as file
import base64
import struct
import soundfile as sf

ws = None
OPENAI_API_KEY=""
headers = [
    "Authorization: Bearer " + OPENAI_API_KEY,
    "OpenAI-Beta: realtime=v1"
]

def update_session():
    session_update = {
        "type": "session.update",
        "session": {
            # "modalities": ["text"],
            # "model": "gpt-4o-realtime-preview",
            # "instructions": "You are a helpful AI assistant. Please answer in a clear and concise manner.",
            "voice": "alloy",
            # "turn_detection": {"type": "server_vad", "threshold": 0.3, "prefix_padding_ms": 300, "silence_duration_ms": 200},
            # "input_audio_format": "pcm16",
            # "output_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": "whisper-1",
                "language": "en",
                "prompt": "make text",
            },
            # "tool_choice": "auto",
            # "temperature": 0.8,
            # "max_response_output_tokens": "inf",
            # "tools": []
        }
    }
    ws.send(json.dumps(session_update))

def _on_open(ws):
    print("Connected to server.")

    update_session()

    audioBase64 = base64_encode_audio("./data/recording.wav")
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

def _on_message(ws, message):
    data = json.loads(message)

    # if data["type"] != "session.created":
    print("Received event:", json.dumps(data, indent=2))

    # if data['type'] == "response.done":
    #     print("RESPONSE:", data['response']['output'][0]['content'][0]['text'])

    # if data.type == "response.done":
    #     print(data.response.output[0])


def _float_to_16bit_pcm(float32_array):
    clipped = [max(-1.0, min(1.0, x)) for x in float32_array]
    pcm16 = b''.join(struct.pack('<h', int(x * 32767)) for x in clipped)
    return pcm16

def base64_encode_audio(path):
    data, samplerate = sf.read(path, dtype='float32')  
    channel_data = data[:, 0] if data.ndim > 1 else data

    pcm_bytes = _float_to_16bit_pcm(channel_data)
    encoded = base64.b64encode(pcm_bytes).decode('ascii')
    return encoded

ws = websocket.WebSocketApp(
    s.openai["REALTIME_MODEL_URL"],
    header=headers,
    on_open=_on_open,
    on_message=_on_message,
)
print("|-- OpenAI realtime websocket connected")

ws.run_forever()