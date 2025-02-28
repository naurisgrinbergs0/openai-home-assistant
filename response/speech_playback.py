from interface import player


# Function to handle speech audio playback
def parallel_speech_playback(audio_queue):
    while True:
        audio = audio_queue.get()
        if audio is None:
            break
        player.play_stream(audio)
