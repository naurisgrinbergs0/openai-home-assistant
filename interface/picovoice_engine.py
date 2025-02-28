from pvrecorder import PvRecorder
import os
import pvporcupine
import settings as s

handle = None
rec = None


def init():
    global handle, rec

    keyword_filename = None
    if s.system["PLATFORM"] == "windows":
        keyword_filename = s.assets["WAKEUP_WORD_WINDOWS_FILE_PATH"]
    elif s.system["PLATFORM"] == "rpi-0w":
        keyword_filename = s.assets["WAKEUP_WORD_RPI_0W_FILE_PATH"]

    handle = pvporcupine.create(
        access_key=os.getenv("PICOVOICE_ACCESS_KEY"),
        keyword_paths=[keyword_filename],
    )
    rec = PvRecorder(512, 0)
    print("|-- Porcupine engine initialized")


def start():
    rec.start()


def process():
    if handle.process(rec.read()) >= 0:
        print("|-- Wakeup word detected")
        return True
    return False


def close():
    handle.delete()
