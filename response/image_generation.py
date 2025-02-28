from openai_api import images


# Function to generate image
async def parallel_image_generation(prompt=None, image=None):
    image_response = None

    if image:
        image_response = images.generate_image_variation(image)
    else:
        image_response = images.generate_image(prompt)

    return image_response
