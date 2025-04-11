# Load environment variables
from dotenv import load_dotenv

# Settings and config
import settings as s
from utility import logger, config, datetime
import json
import time

# Interface
from operations import realtime_event_operations
from interface.audio_recorder import AudioRecorder
from interface.audio_player import AudioPlayer
from interface.wakeword_engine import WakewordEngine
from interface.web_socket import WebSocketInterface

load_dotenv(override=True)

# Initialize / connect
logger.init()
config.init()


def on_wakeword_detected():
    ws_interface_transcribe.start()
    realtime_event_operations.insert_conversation_item(
        ws_interface_transcribe,
        "system",
        text=f"Current time settings: {json.dumps(datetime.get_current_time_settings())}")
    audio_recorder.start_recording()


wakeword_engine = WakewordEngine(on_wakeword_detected_callback=on_wakeword_detected)
audio_player = AudioPlayer()
ws_interface_transcribe = WebSocketInterface(
    s.openai["REALTIME_MODEL_ENDPOINT"],
    realtime_event_operations.get_headers(),
    on_open_callback=realtime_event_operations.update_session,
    on_message_callback=lambda message: realtime_event_operations.on_message(
        message, ws_interface_transcribe, audio_player))
audio_recorder = AudioRecorder(
    on_speech_frame_callback=lambda chunk: realtime_event_operations.send_audio_chunk(ws_interface_transcribe, chunk),
    on_speech_finished_callback=lambda _: (
        realtime_event_operations.commit_audio_chunks(ws_interface_transcribe),
        realtime_event_operations.request_response(ws_interface_transcribe)))

wakeword_engine.start_listening()

input()

ws_interface_transcribe.stop()
wakeword_engine.stop()
audio_recorder.stop_recording()
