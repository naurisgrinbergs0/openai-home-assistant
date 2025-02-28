import soundfile as sf
import sounddevice as sd
import io


def play_stream(spoken_response):
    buffer = io.BytesIO()
    for chunk in spoken_response.iter_bytes(chunk_size=4096):
        buffer.write(chunk)
    buffer.seek(0)

    with sf.SoundFile(buffer, "r") as sound_file:
        data = sound_file.read(dtype="int16")
        sd.play(data, sound_file.samplerate)
        sd.wait()


def play_file(filename, sync=True):
    with sf.SoundFile(filename, "r") as sound_file:
        data = sound_file.read(dtype="int16")
        sd.play(data, sound_file.samplerate)
        if sync:
            sd.wait()
