import pyaudio
import audioop
import time
import wave
import utility.config as config

audio = None

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 24000
CHUNK = 1024

# TODO: play with rms value and decide the best
# TODO: implement functionality - when assistant woken up, start listening immediately to prompt
# (i think this will only work if wakeup feedback is a sound, if it's a phrase then it will pick up it's own speech)


def init():
    global audio
    audio = pyaudio.PyAudio()


def record_prompt():
    stream = audio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    frames = []
    frames_recorded = 0
    last_quiet_start_time = None
    recording_start_time = None
    waiting_start_time = time.time()

    # Loop until waiting time timeout is reached or max recording duration reached
    while (
        recording_start_time == None and (time.time() - waiting_start_time) < 10
    ) or (recording_start_time != None and (time.time() - recording_start_time) < 10):
        frame = stream.read(CHUNK)
        is_quiet = audioop.rms(frame, 2) < 300

        # If volume is high - start recording
        if recording_start_time == None and not is_quiet:
            recording_start_time = time.time()
            print("|-- Recording started")
        elif recording_start_time != None:
            frames.append(frame)
            frames_recorded += 1

            # If it is quiet - store quietness start time
            if is_quiet and last_quiet_start_time == None:
                last_quiet_start_time = time.time()
            elif not is_quiet:
                last_quiet_start_time = None

            # If it's been quiet for some time - exit loop
            if (
                last_quiet_start_time != None
                and (time.time() - last_quiet_start_time) > 2
            ):
                break

    # Store recording to file
    wf = wave.open(config.get_data_file_path("RECORDING_FILE_NAME"), "wb")
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b"".join(frames))
    wf.close()

    stream.stop_stream()
    stream.close()
    print("|-- Recording finished")

    return recording_start_time != None
