import settings as s
from openai_api.connection import client
import utility.config as config


def transcribe():
    audio_file = open(config.get_data_file_path("RECORDING_FILE_NAME"), "rb")
    transcript = client.audio.transcriptions.create(
        model=s.openai["TRANSCRIPT_MODEL"],
        file=audio_file,
        response_format="text",
        language=s.locale["LANGUAGE_CODE"],
    )
    return transcript
