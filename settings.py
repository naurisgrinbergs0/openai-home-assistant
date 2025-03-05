# Functions
functions = {
    "GET_WEATHER": "get_weather",
    "TAKE_PICTURE": "take_picture",
    "TOGGLE_LIGHTS": "toggle_lights",
    "TELEGRAM_SEND_MESSAGE": "telegram_send_message",
    "TELEGRAM_SEND_PICTURE": "telegram_send_picture",
    "GET_USER_INPUT": "get_user_input",
}

# Assets
assets = {
    "WAKEUP_WORD_WINDOWS_FILE_PATH": "./assets/wakeup_phrases/hey-alex-windows.ppn",
    "WAKEUP_WORD_RPI_0W_FILE_PATH": "./assets/wakeup_phrases/nelson-rpi-0w.ppn",
    "WAKEUP_SOUND_FILE_PATH": "./assets/wakeup_sounds/event.mp3",
}

# Data
data = {
    "DATA_FOLDER_PATH": "./data",
    "CONFIG_FILE_NAME": "config.json",
    "CAPTURE_FILE_NAME": "capture.png",
    "RECORDING_FILE_NAME": "recording.mp3",
    "IMAGE_FILE_NAME": "image.jpg",
    "LOG_FILE_NAME": "log.log",
}

# System settings
system = {
    "PLATFORM": "windows",  # Options: ("windows" | "rpi-0w")
    "LOGGING_ENABLED": True,
}

# API endpoints
api = {
    "VISUAL_CROSSING_WEATHER_BASE_URL":
        "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline",
}

# Locale settings
locale = {
    "UNIT_SYSTEM": "metric",  # Options: ("metric" | "imperial")
    "LANGUAGE_CODE": "lv",  # 2 symbol code
}

# OpenAI settings
openai = {
    "TRANSCRIPT_MODEL": "whisper-1",
    "SPEECH_MODEL": "tts-1",
    "COMPLETIONS_MODEL": "gpt-4-turbo-preview",
    "VISION_MODEL": "gpt-4-vision-preview",
    "IMAGE_MODEL": "dall-e-3",
    "IMAGE_VARIATION_MODEL": "dall-e-2",
    "SPEECH_VOICE": "nova",
    "CONVERSATION_CONTEXT_MESSAGE_COUNT": 10,
    "CONVERSATION_RESPONSE_MAX_TOKEN_COUNT": 300,
    "IMAGE_DIMENSIONS": "1024x1024",
    "REALTIME_MODEL_URL": "wss://api.openai.com/v1/realtime?model=gpt-4o-realtime-preview-2024-12-17"
}

# Settings related to audio processing
audio = {
    "INPUT_AUDIO_SAMPLE_RATE": 32000,
    "INPUT_AUDIO_FRAME_DURATION": 20,  # Options: (10 | 20 | 30)
    "INPUT_AUDIO_VOICE_ACTIVITY_DETECTION_AGGRESSIVENESS": 2,  # Integer in range: [0, 3]
    "INPUT_AUDIO_MAX_WAIT_DURATION_SECONDS": 6,
    "INPUT_AUDIO_MAX_RECORD_DURATION_SECONDS": 30,
    "INPUT_AUDIO_SILENCE_DURATION_SECONDS": 1,
}
