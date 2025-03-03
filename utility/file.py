import base64
import requests


def save_url_file(url, path):
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        with open(path, "wb") as f:
            f.write(response.content)


def read_file_bytes(path):
    with open(path, "rb") as file:
        data = file.read()
    return data


def read_file_base64(path):
    with open(path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")
