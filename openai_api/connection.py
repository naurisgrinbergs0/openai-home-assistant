import os
from openai import OpenAI

client = None


def init():
    global client
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("|-- OpenAI client connected")
