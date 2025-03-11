import threading
import time
import wave
import pyaudio
import webrtcvad
import settings as s
from utility import config


class AudioRecorder:

    def __init__(
            self, on_speech_started_callback=None, on_speech_frame_callback=None, on_speech_finished_callback=None):
        self.on_speech_frame_callback = on_speech_frame_callback
        self.on_speech_started_callback = on_speech_started_callback
        self.on_speech_finished_callback = on_speech_finished_callback
        self.audio = pyaudio.PyAudio()
        self.sample_rate = s.audio["INPUT_AUDIO_SAMPLE_RATE"]
        self.frame_duration_ms = s.audio["INPUT_AUDIO_FRAME_DURATION"]
        self.frame_size = int(self.sample_rate * (self.frame_duration_ms / 1000.0) * 2)
        self.vad = webrtcvad.Vad(s.audio["INPUT_AUDIO_VOICE_ACTIVITY_DETECTION_AGGRESSIVENESS"])
        self.max_wait_duration = s.audio["INPUT_AUDIO_MAX_WAIT_DURATION_SECONDS"]
        self.max_record_duration = s.audio["INPUT_AUDIO_MAX_RECORD_DURATION_SECONDS"]
        self.silence_duration = s.audio["INPUT_AUDIO_SILENCE_DURATION_SECONDS"]
        self.recording_thread = None
        self.stop_event = threading.Event()

    def start_recording(self):
        self.stop_event.clear()
        self.recording_thread = threading.Thread(target=self._record)
        self.recording_thread.start()

    def stop_recording(self):
        self.stop_event.set()
        if self.recording_thread:
            self.recording_thread.join()

    def _record(self):
        stream = self.audio.open(
            format=pyaudio.paInt16, channels=1, rate=self.sample_rate, input=True, frames_per_buffer=self.frame_size)

        frames = []
        recording_started = False
        silence_start_time = None
        waiting_start_time = time.time()
        recording_start_time = None

        print("|-- Listening for sound using VAD")

        while not self.stop_event.is_set():
            current_time = time.time()

            # If max wait time exceeded - exit
            if not recording_started and (current_time - waiting_start_time) >= self.max_wait_duration:
                print("|-- Max wait time exceeded, no speech detected")
                break

            # If max record duration exceeded, stop recording
            if recording_started and (current_time - recording_start_time) >= self.max_record_duration:
                print("|-- Max record time reached.")
                break

            try:
                frame = stream.read(self.frame_size, exception_on_overflow=False)
            except Exception as e:
                print(f"|-- Error reading audio: {e}")
                continue

            # Check if frame contains speech using VAD
            is_speech = self.vad.is_speech(frame, self.sample_rate, length=640)

            # Start recording when speech is detected
            if not recording_started and is_speech:
                recording_started = True
                recording_start_time = current_time
                if self.on_speech_started_callback:
                    self.on_speech_started_callback()
                print("|-- Recording started")

            if recording_started:
                frames.append(frame)
                # Invoke the external callback with the current frame
                if self.on_speech_frame_callback:
                    self.on_speech_frame_callback(frame)

                # Check for prolonged silence to determine if we should stop recording
                if not is_speech:
                    if silence_start_time is None:
                        silence_start_time = current_time
                    elif (current_time - silence_start_time) > self.silence_duration:
                        if self.on_speech_finished_callback:
                            self.on_speech_finished_callback(b"".join(frames))
                        print("|-- Recording stopped due to silence")
                        break
                else:
                    silence_start_time = None

        # Save the recorded audio to a file
        recording_path = config.get_data_file_path("RECORDING_FILE_NAME")
        wf = wave.open(recording_path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.sample_rate)
        wf.writeframes(b"".join(frames))
        wf.close()

        stream.stop_stream()
        stream.close()
        print("|-- Recording finished")
