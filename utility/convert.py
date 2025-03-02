import base64


def bytes_to_base64(data):
    return base64.b64encode(data).decode('ascii')


def base64_to_bytes(data):
    return base64.b64decode(data)
