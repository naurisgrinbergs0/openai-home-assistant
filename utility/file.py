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