from openai_api import speech


# Function to process speech generation
def parallel_speech_generation(phrase_queue, audio_queue):
    while True:
        phrase = phrase_queue.get()
        if phrase is None:
            audio_queue.put(None)  # Signal the end of the audio
            break
        response = speech.generate_speech(phrase)
        audio_queue.put(response)
