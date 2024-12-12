import os
from typing import List

import google.generativeai as genai
import PIL.Image

from medical_database import MedicalDatabase


class GeminiModel:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.temperature = 0.
        self.history = []
        self.rag_database = MedicalDatabase()

    def rag(self, prompt: str) -> str:
        results = self.rag_database.get_query_results(prompt)
        rag_prompt = ""
        if len(results) > 0:
            for result in results:
                text = result['text']
                rag_prompt = rag_prompt + text
        return rag_prompt

    def get_response(self, prompt: str, images: List[str] = None, history: List = None) -> str:
        chat = self.model.start_chat(history=history)
        inputs = [prompt]
        if images:
            for image in images:
                image_base64 = PIL.Image.open(image)
                inputs.append(image_base64)
        response = chat.send_message(inputs)
        return response.text

