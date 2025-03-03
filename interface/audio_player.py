import pyaudio


class AudioPlayer:

    def __init__(self):
        self.player = pyaudio.PyAudio()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 24000
        self.chunk_size = 1024

        # Internal buffer to store incoming audio bytes
        self.audio_buffer = bytearray()

        # Initialize the stream
        self.stream = None

    def append_audio_chunks(self, data):
        self.audio_buffer.extend(data)

        # Try to ensure the stream is running.
        try:
            if not self.stream.is_active():
                self.stream.start_stream()
        except Exception:
            # If the stream has been closed or an error occurs, reopen it.
            self._open_stream()
            self.stream.start_stream()

    def stop_playing(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.player.terminate()

    def _open_stream(self):
        self.stream = self.player.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            output=True,
            frames_per_buffer=self.chunk_size,
            stream_callback=self._stream_callback)

    def _stream_callback(self, _in_data, frame_count, _time_info, _status):
        # Calculate number of bytes needed (2 bytes per frame for paInt16)
        bytes_needed = frame_count * 2
        current_buffer_size = len(self.audio_buffer)

        if current_buffer_size >= bytes_needed:
            # Provide the required number of bytes
            audio_chunk = bytes(self.audio_buffer[:bytes_needed])
            self.audio_buffer = self.audio_buffer[bytes_needed:]
        else:
            # Not enough data; pad with silence (zeros)
            audio_chunk = bytes(self.audio_buffer) + b'\x00' * (bytes_needed - current_buffer_size)
            self.audio_buffer = bytearray()

        return (audio_chunk, pyaudio.paContinue)
