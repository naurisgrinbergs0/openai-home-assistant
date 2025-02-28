import threading
from queue import Queue
from response.phrase_generation import parallel_phrase_generation
from response.speech_generation import parallel_speech_generation
from response.speech_playback import parallel_speech_playback


phrase_queue = Queue()
audio_queue = Queue()
is_generating_speech = True


def respond_in_realtime_async(
    prompt, capture_base64=None, tool_call_id_replying_to=None
):
    phrase_thread = threading.Thread(
        target=parallel_phrase_generation,
        args=(
            phrase_queue,
            prompt,
            capture_base64,
            tool_call_id_replying_to,
        ),
    )
    speech_thread = threading.Thread(
        target=parallel_speech_generation,
        args=(
            phrase_queue,
            audio_queue,
        ),
    )
    playback_thread = threading.Thread(
        target=parallel_speech_playback, args=(audio_queue,)
    )

    phrase_thread.start()
    speech_thread.start()
    playback_thread.start()
