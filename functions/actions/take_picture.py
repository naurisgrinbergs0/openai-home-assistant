from interface import camera
from utility import config, file


def take_picture(called_function):
    camera.take_picture(config.get_data_file_path("CAPTURE_FILE_NAME"))
    image_base64 = file.read_file_base64(config.get_data_file_path("CAPTURE_FILE_NAME"))
    # TODO: send image to completions api with prompt
    # get description
    # return standartized result
