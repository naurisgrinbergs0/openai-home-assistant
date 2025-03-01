import base64
import struct
import soundfile as sf

# def _float_to_16bit_pcm(float32_array):
#     clipped = [max(-1.0, min(1.0, x)) for x in float32_array]
#     pcm16 = b''.join(struct.pack('<h', int(x * 32767)) for x in clipped)
#     return pcm16

# def base64_encode_audio(path):
#     data, samplerate = sf.read(path, dtype='float32')  
#     channel_data = data[:, 0] if data.ndim > 1 else data

#     pcm_bytes = _float_to_16bit_pcm(channel_data)
#     encoded = base64.b64encode(pcm_bytes).decode('ascii')
#     return encoded

def bytes_to_base64(data):
    return base64.b64decode(data).decode('ascii')

def base64_to_bytes(data):
    return base64.b64decode(data)