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
ws_thread = threading.Thread(target=realtime.start, daemon=True)
ws_thread.start()
time.sleep(1)




cnt = 0
while True:
    try:
        if cnt == 0:
        # if picovoice_engine.process():
            # time.sleep(0.4)
            # player.play_file(s.assets["WAKEUP_SOUND_FILE_PATH"])
            prompt_recorded = recorder.record_prompt()

            # print("TRANS: ", transcripts.transcribe())

            if prompt_recorded:
                realtime.send_message()
                cnt += 1
    # except FunctionError as err:
    #     e(err.message, True)
    # except Exception as err:
    #     e(f"Unhandled exception occured: {err}", True)
    except KeyboardInterrupt:
        break
exit()