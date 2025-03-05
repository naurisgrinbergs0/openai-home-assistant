# Load environment variables
from dotenv import load_dotenv

# Settings and config
import settings as s
from utility import logger, config, datetime
import json

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
    ws_interface.start()
    realtime_event_operations.insert_conversation_text(
        ws_interface, "system", f"Current time settings: {json.dumps(datetime.get_current_time_settings())}")
    # realtime_event_operations.insert_conversation_text(
    #     ws_interface, "user",
    #     "Ja tu gribi saņemt atbildi uz tavu jautājumu, tad obligāti pievieno tool call get_user_input reizē ar jautājumu."
    # )
    realtime_event_operations.insert_conversation_text(ws_interface, "user", "Domāju kur aizbraukt")
    realtime_event_operations.request_response(ws_interface)
    # audio_recorder.start_recording()


wakeword_engine = WakewordEngine(on_wakeword_detected_callback=on_wakeword_detected)
audio_player = AudioPlayer()
ws_interface = WebSocketInterface(
    s.openai["REALTIME_MODEL_URL"],
    realtime_event_operations.get_headers(),
    on_open_callback=realtime_event_operations.update_session,
    on_message_callback=lambda message: realtime_event_operations.on_message(message, ws_interface, audio_player))
audio_recorder = AudioRecorder(
    on_speech_frame_callback=lambda chunk: realtime_event_operations.send_audio_chunk(ws_interface, chunk),
    on_speech_finished_callback=lambda: (
        realtime_event_operations.commit_audio_chunks(ws_interface),
        realtime_event_operations.request_response(ws_interface)))

on_wakeword_detected()
# wakeword_engine.start_listening()

input()

ws_interface.stop()
wakeword_engine.stop()
audio_recorder.stop_recording()
