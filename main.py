# Load environment variables
from dotenv import load_dotenv

load_dotenv(override=True)

# Settings and config
import settings as s
import time
from utility.error import FunctionError
from utility.logger import e
import utility.config as config
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
openai_api.connection.init()
config.init()
# picovoice_engine.init()
recorder.init()
realtime.init()

# picovoice_engine.start()




stop_flag = False

def on_message(ws, message):
    print("Received:", message)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    print("Connection closed:", close_status_code, close_msg)

def on_open(ws):
    print("Connection opened")

def action_loop(ws):
    global stop_flag
    while not stop_flag:
        prompt_recorded = recorder.record_prompt()
        ws.send("Event X occurred")
        if prompt_recorded:
                realtime.send_message()
        stop_flag = True
    ws.close()

def wait_for_exit():
    global stop_flag
    input("Press Enter to exit...\n")
    stop_flag = True

ws_app = websocket.WebSocketApp(
    "ws://echo.websocket.events",
    on_message=on_message,
    on_error=on_error,
    on_close=on_close
)
ws_app.on_open = on_open

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


while True:
    try:
        # if picovoice_engine.process():
            # time.sleep(0.4)
            # player.play_file(s.assets["WAKEUP_SOUND_FILE_PATH"])
            prompt_recorded = recorder.record_prompt()

            # print("TRANS: ", transcripts.transcribe())

            if prompt_recorded:
                realtime.send_message()
    # except FunctionError as err:
    #     e(err.message, True)
    # except Exception as err:
    #     e(f"Unhandled exception occured: {err}", True)
    except KeyboardInterrupt:
        break
exit()