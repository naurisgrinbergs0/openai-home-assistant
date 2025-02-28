from openai_api.connection import client
import settings as s


def generate_image(prompt):
    result = client.images.generate(
        model=s.openai["IMAGE_MODEL"],
        prompt=prompt,
        n=1,
        size=s.openai["IMAGE_DIMENSIONS"],
    )
    return result


def generate_image_variation(image):
    result = client.images.create_variation(
        # image=open(config.get_data_file_path("CAPTURE_FILE_NAME"), "rb"),
        image=image,
        model=s.openai["IMAGE_VARIATION_MODEL"],
        n=1,
        size=s.openai["IMAGE_DIMENSIONS"],
    )
    return result
