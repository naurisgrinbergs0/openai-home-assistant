import json
import settings as s
import os
import utility.config as config

data_folder_path = s.data["DATA_FOLDER_PATH"]

# TODO: globally add try .. except


def init():
    if not os.path.exists(data_folder_path):
        os.mkdir(data_folder_path)


def store_config(key, value):
    try:
        with open(get_data_file_path("CONFIG_FILE_NAME"), "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data[key] = value

    with open(get_data_file_path("CONFIG_FILE_NAME"), "w") as file:
        json.dump(data, file)


def retrieve_config(key):
    try:
        with open(get_data_file_path("CONFIG_FILE_NAME"), "r") as file:
            data = json.load(file)
            return data.get(key)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return None


def get_data_file_path(key):
    return os.path.join(data_folder_path, s.data[key])
