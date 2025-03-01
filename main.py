# Load environment variables
from dotenv import load_dotenv

load_dotenv(override=True)

# Settings and config
import os
import time
import settings as s
from utility import config
from utility import logger
from utility.error import FunctionError
import threading
import websocket

# Interface
from openai_api import realtime
import openai_api.connection
import interface.picovoice_engine as picovoice_engine
import interface.recorder as recorder
import interface.player as player
from openai_api import transcripts

# Initialize / connect
logger.init()
# openai_api.connection.init()
config.init()
# picovoice_engine.init()
recorder.init()
# realtime.init()

# picovoice_engine.start()




stop_flag = False
connected_event = threading.Event()

def on_message(ws, message):
    realtime.on_message(ws, message)

def on_error(ws, error):
    print("|-- OpenAI WebSocket error:", error)

def on_close(ws, close_status_code, close_msg):
    print("|-- OpenAI WebSocket disconnected:", close_status_code, close_msg)

def on_open(ws):
    connected_event.set()
    print("|-- OpenAI WebSocket connected")

def action_loop(ws):
    global stop_flag
    connected_event.wait()
    while not stop_flag:
        prompt_recorded = recorder.record_prompt()
        time.sleep(2)

        if prompt_recorded:
            realtime.send_message(ws)
            time.sleep(10)
        stop_flag = True
    ws.close()

def wait_for_exit():
    global stop_flag
    input()
    stop_flag = True

ws_app = websocket.WebSocketApp(
    s.openai["REALTIME_MODEL_URL"],
    header = [
        "Authorization: Bearer " + os.getenv("OPENAI_API_KEY"),
        "OpenAI-Beta: realtime=v1"
    ],
    on_open=on_open,
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)

# Start a thread that runs the action loop
action_thread = threading.Thread(target=action_loop, args=(ws_app,))
action_thread.daemon = True  # Optional: make thread exit if main thread exits
action_thread.start()

# Start a thread that waits for the user to press Enter
exit_thread = threading.Thread(target=wait_for_exit)
exit_thread.daemon = True
exit_thread.start()

# This call will block and keep receiving WebSocket events
ws_app.run_forever()