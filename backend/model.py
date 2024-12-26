import os
from typing import List

import google.generativeai as genai
from volcenginesdkarkruntime import Ark
import PIL.Image
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from medical_database import MedicalDatabase


class GeminiModel:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.temperature = 0.
        self.history = []
        self.rag_database = MedicalDatabase()

    def rag(self, prompt: str, history=None) -> str:
        if history:
            for record in history:
                if record['sender'] == 'user':
                    prompt = record['text'] + " " + prompt
        results = self.rag_database.get_query_results(prompt)
        rag_prompt = ""
        if len(results) > 0:
            for result in results:
                text = result['text']
                rag_prompt = rag_prompt + text
        return rag_prompt

    def get_response(self, prompt: str, images: List[str] = None, history: List = None) -> str:
        history = [
            {'role': 'model' if entry['sender'] == 'bot' else entry['sender'], 'parts': entry['text']}  # bot/user
            for entry in history
        ]
        chat = self.model.start_chat(history=history)
        inputs = [prompt]
        if images:
            for image in images:
                image_base64 = PIL.Image.open(image)
                inputs.append(image_base64)
        response = chat.send_message(inputs)
        return response.text


class DoubaoModel:
    def __init__(self):
        # export VOLC_ACCESSKEY=***
        # export VOLC_SECRETKEY=***
        self.client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            region="cn-beijing"
        )
        self.model = "ep-20241225201942-9vppj"
        self.history = []
        self.rag_database = MedicalDatabase()

    def rag(self, prompt: str, history=None) -> str:
        if history:
            for record in history:
                if record['sender'] == 'user':
                    prompt = record['text'] + " " + prompt
        results = self.rag_database.get_query_results(prompt)
        rag_prompt = ""
        if len(results) > 0:
            for result in results:
                text = result['text']
                rag_prompt = rag_prompt + text
        return rag_prompt

    def get_response(self, prompt: str, history: List = None) -> str:
        messages = [
            {'role': 'system' if entry['sender'] == 'bot' else entry['sender'], 'content': entry['text']}     # bot/user
            for entry in history
        ]
        messages.append({'role': 'user', 'content': prompt})
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            extra_headers={'x-is-encrypted': 'true'},
        )
        response = completion.choices[0].message.content
        return response


# OBSOLETE
class LocalModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("qsy71/4-bit_medical_LLaMA3-8B-Chinese-Chat")
        self.model = AutoModelForCausalLM.from_pretrained("qsy71/4-bit_medical_LLaMA3-8B-Chinese-Chat")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
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

    def get_response(self, prompt: str, history: List = None) -> str:
        history = [
            {'role': 'model' if entry['sender'] == 'bot' else entry['sender'], 'content': entry['text']}
            for entry in history
        ]
        messages = history.append({'role': 'user', 'content': prompt})
        with torch.no_grad():
            data_input = self.tokenizer(messages, return_tensors="pt", padding=True).to(self.device)
            data_output = self.model(**data_input, output_hidden_states=True)
        response = data_output
        return response.text

