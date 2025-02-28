import interface.camera as camera
from utility import config, file
from response import response
from openai_api import configuration


# TODO: check if possible to respond with role=tool to a visual openai prompt


def take_picture(called_function, prompt):
    camera.take_picture(config.get_data_file_path("CAPTURE_FILE_NAME"))
    image_base64 = file.read_file_base64(config.get_data_file_path("CAPTURE_FILE_NAME"))

    response.respond_in_realtime_async(
        prompt + f"|{configuration.assistant_respond_shortly}",
        image_base64,
        tool_call_id_replying_to=called_function.call_id,
    )
