# Load environment variables
from dotenv import load_dotenv

# Settings and config
import settings as s
from utility import config
from utility import logger

# Interface
from openai_api import realtime
from interface.audio_recorder import AudioRecorder
from interface.wakeword_engine import WakewordEngine
from interface.web_socket import WebSocketInterface

load_dotenv(override=True)

# Initialize / connect
logger.init()
config.init()
ws_interface = WebSocketInterface(
    s.openai["REALTIME_MODEL_URL"],
    realtime.get_headers(),
    on_open_callback=realtime.update_session,
    on_message_callback=realtime.on_message)
wakeword_engine = WakewordEngine()
audio_recorder = AudioRecorder(
    on_speech_frame_callback=lambda chunk: realtime.send_audio_chunk(ws_interface, chunk),
    on_speech_finished_callback=lambda:
    (realtime.commit_audio_chunks(ws_interface), realtime.request_response(ws_interface)))

ws_interface.start()
wakeword_engine.start()

while True:
    if wakeword_engine.is_wakeword_detected():
        audio_recorder.start_recording()

ws_interface.stop()
wakeword_engine.close()
audio_recorder.start_recording()
