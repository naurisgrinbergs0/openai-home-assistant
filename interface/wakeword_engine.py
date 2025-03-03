import os
from pvrecorder import PvRecorder
import pvporcupine
import settings as s


class WakewordEngine:

    def __init__(self):
        # Select the appropriate keyword file based on the platform.
        keyword_filename = s.assets["WAKEUP_WORD_WINDOWS_FILE_PATH"]

        # Initialize the Porcupine engine.
        self.engine = pvporcupine.create(
            access_key=os.getenv("PICOVOICE_ACCESS_KEY"),
            keyword_paths=[keyword_filename],
        )

        # Initialize the recorder.
        self.rec = PvRecorder(frame_length=512, device_index=0)
        print("|-- Porcupine engine initialized")

    def start(self):
        self.rec.start()

    def is_wakeword_detected(self):
        audio_frame = self.rec.read()
        if self.engine.process(audio_frame) >= 0:
            print("|-- Wakeup word detected")
            return True
        return False

    def close(self):
        self.engine.delete()
