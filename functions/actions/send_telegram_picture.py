import interface.camera as camera
from utility import config, file
from telegram_api import messaging, recipients
from response import image_generation


async def generate_image(called_function):
    image = None

    if called_function.arguments.get("image_source_for_variation") == "camera":
        camera.take_picture(config.get_data_file_path("CAPTURE_FILE_NAME"))
        image = file.read_file_bytes(config.get_data_file_path("CAPTURE_FILE_NAME"))
    elif (
        called_function.arguments.get("image_source_for_variation") == "previous_image"
    ):
        pass  # TODO: finish

    generated_image = await image_generation.parallel_image_generation(
        called_function.arguments.get("prompt"),
        image,
    )

    post_action = called_function.arguments.get("post_action_send_telegram_message")
    if post_action:
        users = recipients.find_recipients(
            chat_ids=recipients.parse_recipient_array(post_action.get("recipients"))
        )

        await messaging.send_image(
            users, generated_image.data[0].url, generated_image.data[0].revised_prompt
        )
