from interface import camera
from utility import config, file


async def take_picture(function_data):
    response = None

    try:
        camera.take_picture(config.get_data_file_path("CAPTURE_FILE_NAME"))
        image_base64 = file.read_file_base64(config.get_data_file_path("CAPTURE_FILE_NAME"))

        # TODO: send image to completions api with prompt
        # TODO: get description

    except Exception:
        return (None, "Unknown error")

    return (response, None)
