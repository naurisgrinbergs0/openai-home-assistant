import settings as s
from openai_api.connection import client
import utility.config as config


def generate_speech(text):
    response = client.audio.speech.create(
        model=s.openai["SPEECH_MODEL"],
        voice=s.openai["SPEECH_VOICE"],
        input=text,
    )

    return response
