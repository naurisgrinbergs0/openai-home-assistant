# Load environment variables
from dotenv import load_dotenv

load_dotenv(override=True)

# Settings and config
import settings as s
import time
from utility.error import FunctionError
from utility.logger import e
import utility.config as config

# API connection
import openai_api.connection
import telegram_api.connection

openai_api.connection.init()
telegram_api.connection.init()

# Interface
from response import response
from openai_api import transcripts
import interface.picovoice_engine as picovoice_engine
import interface.recorder as recorder
import interface.player as player


# Initialize / connect
config.init()
picovoice_engine.init()
recorder.init()

picovoice_engine.start()
telegram_api.connection.start()

# TODO: i guess, now i can interrupt assistant while it is talking, but right now, i think threads/other async processes wont be stopped - should stop

prompt_executed = False
test_phrase = None#"Kā iet?"

# Mainloop
while True:
    try:
        if picovoice_engine.process():
            time.sleep(0.4)
            player.play_file(s.assets["WAKEUP_SOUND_FILE_PATH"])
            prompt_recorded = recorder.record_prompt()

            if prompt_recorded:
                transcript = transcripts.transcribe()
                print(transcript)
                if str(transcript).strip() != "":
                    response.respond_in_realtime_async(transcript)
    except FunctionError as err:
        e(err.message, True)
    except Exception as err:
        e(f"Unhandled exception occured: {err}", True)

    if test_phrase and not prompt_executed:
        print("!! Running test phrase")
        prompt_executed = True
        response.respond_in_realtime_async(test_phrase)
