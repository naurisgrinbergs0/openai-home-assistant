# Functions
functions = {
    "TOGGLE_LIGHTS": "toggle_lights",
    "TAKE_PICTURE": "take_picture",
    "GET_WEATHER": "get_weather",
    "GENERATE_IMAGE": "generate_image",
}

# Assets
assets = {
    "WAKEUP_WORD_WINDOWS_FILE_PATH": "./assets/wakeup_phrases/hej-bobbie-windows.ppn",
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

# Platform
system = {
    "PLATFORM": "windows",  # Options: ("windows" | "rpi-0w")
    "LOGGING_ENABLED": True,
}

# API endpoints
api = {
    "VISUAL_CROSSING_WEATHER_BASE_URL": "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline",
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
