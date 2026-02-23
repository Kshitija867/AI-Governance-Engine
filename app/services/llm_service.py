import requests

class LLMService:

    def __init__(self, model_name="qwen2.5:3b"):
        self.base_url = "http://localhost:11434/api/generate"
        self.model_name = model_name

    def generate(self, prompt: str, temperature: float = 0.2):

        payload = {
            "model": self.model_name,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        response = requests.post(self.base_url, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama Error: {response.text}")

        return response.json()["response"]