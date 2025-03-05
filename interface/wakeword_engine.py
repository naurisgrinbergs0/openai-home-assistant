import os
import threading
from pvrecorder import PvRecorder
import pvporcupine
import settings as s


class WakewordEngine:

    def __init__(self, on_wakeword_detected_callback):
        self.is_listening = threading.Event()
        self.on_wakeword_detected_callback = on_wakeword_detected_callback

        # Select the appropriate keyword file based on the platform.
        keyword_filename = s.assets["WAKEUP_WORD_WINDOWS_FILE_PATH"]

        # Initialize the Porcupine engine.
        self.engine = pvporcupine.create(
            access_key=os.getenv("PICOVOICE_ACCESS_KEY"), keyword_paths=[keyword_filename], sensitivities=[0.7])

        # Initialize the recorder.
        # TODO: mby change params for better activation
        self.rec = PvRecorder(frame_length=self.engine.frame_length, device_index=0)
        print("|-- Porcupine engine initialized")

    def start_listening(self):
        self.is_listening.set()
        self.rec.start()

        def process_frame():
            while self.is_listening:
                audio_frame = self.rec.read()
                if self.engine.process(audio_frame) >= 0:
                    print("|-- Wakeup word detected")
                    self.on_wakeword_detected_callback()

        ws_thread = threading.Thread(target=process_frame, args=())
        ws_thread.daemon = True
        ws_thread.start()

    def stop(self):
        self.is_listening.clear()
        self.engine.delete()
