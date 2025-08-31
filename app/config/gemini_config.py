import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")

gemini_genai_client = genai.Client(api_key=api_key)
