import requests
import base64
import struct
import soundfile as sf


def save_url_file(url, path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)


def read_file_bytes(path):
    with open(path, "rb") as file:
        bytes = file.read()
    return bytes


def read_file_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")


def _float_to_16bit_pcm(float32_array):
    clipped = [max(-1.0, min(1.0, x)) for x in float32_array]
    pcm16 = b''.join(struct.pack('<h', int(x * 32767)) for x in clipped)
    return pcm16

def base64_encode_audio(path):
    data, samplerate = sf.read(path, dtype='float32')  
    channel_data = data[:, 0] if data.ndim > 1 else data

    pcm_bytes = _float_to_16bit_pcm(channel_data)
    encoded = base64.b64encode(pcm_bytes).decode('ascii')
    return encoded