from interface import camera
from utility import config, file
from telegram_api import messaging, recipients


async def send_telegram_picture(function_data):
    image = None
    prompt = None

    try:
        match function_data.arguments.get("source"):
            case "generate":
                prompt = function_data.arguments.get("prompt")
                #     image_for_variation = None
                #     if function_data.arguments.get("image_source_for_variation") == "camera":
                #         camera.take_picture(config.get_data_file_path("CAPTURE_FILE_NAME"))
                #         image_for_variation = file.read_file_bytes(config.get_data_file_path("CAPTURE_FILE_NAME"))

                #     elif (function_data.arguments.get("image_source_for_variation") == "previous_image"):
                #         pass  # TODO: finish

                #     generated_image = await generate(
                #         function_data.arguments.get("prompt"),
                #         image_for_variation,
                #     )
            case "capture":
                prompt = "Uzņemtais fotoattēls"  # TODO: add to settings mby
                camera.take_picture(config.get_data_file_path("CAPTURE_FILE_NAME"))
                image = file.read_file_bytes(config.get_data_file_path("CAPTURE_FILE_NAME"))
            case "recent_image":
                prompt = "Pēdējais attēls"  # TODO: add to settings mby
                image = file.read_file_bytes(config.get_data_file_path("CAPTURE_FILE_NAME"))

        users = recipients.find_recipients(
            chat_ids=recipients.parse_recipient_array(function_data.arguments.get("recipients")))
        await messaging.send_image(users, image, prompt)

    except Exception:
        return (None, "Unknown error")

    return ("success", None)
