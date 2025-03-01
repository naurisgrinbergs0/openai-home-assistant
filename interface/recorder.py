import pyaudio
import wave
import time
import webrtcvad
import utility.config as config
import settings as s

audio = None

def init():
    global audio
    audio = pyaudio.PyAudio()

def record_prompt():
    sample_rate = s.device["INPUT_AUDIO_SAMPLE_RATE"]
    frame_duration_ms = 20
    frame_size = int(sample_rate * (frame_duration_ms / 1000.0) * 2)

    stream = audio.open(
        format=pyaudio.paInt16, channels=1, rate=sample_rate,
        input=True, frames_per_buffer=frame_size
    )

    vad = webrtcvad.Vad(2)

    frames = []
    recording_started = False
    silence_start_time = None
    waiting_start_time = time.time()

    print("|-- Listening for sound using VAD")
    max_wait_time = 6
    max_record_time = 30

    recording_start_time = None

    while ((not recording_started and (time.time() - waiting_start_time) < max_wait_time) or
           (recording_started and (time.time() - recording_start_time) < max_record_time)):
        frame = stream.read(frame_size)
        # VAD expects 16-bit mono PCM.
        is_speech = vad.is_speech(frame, sample_rate, length=640)

        # Start recording when speech is detected
        if not recording_started and is_speech:
            recording_started = True
            recording_start_time = time.time()
            print("|-- Recording started")

        if recording_started:
            frames.append(frame)

            # Check for silence: if VAD reports non-speech continuously
            if not is_speech:
                if silence_start_time is None:
                    silence_start_time = time.time()
                # If silence persists for longer than threshold (e.g., 1 second), stop
                elif (time.time() - silence_start_time) > 1.0:
                    print("|-- Detected prolonged silence. Stopping recording.")
                    break
            else:
                silence_start_time = None

    # Save the recorded audio to a file.
    wf = wave.open(config.get_data_file_path("RECORDING_FILE_NAME"), "wb")
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b"".join(frames))
    wf.close()

    stream.stop_stream()
    stream.close()
    print("|-- Recording finished")

    return recording_started