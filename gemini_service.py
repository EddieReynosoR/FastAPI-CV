import os

from google import genai
from google.genai import types

class GeminiService:
    def __init__(self, model: str = "gemini-3-flash-preview") -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY.")
        
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def test_prompt(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.3
            )
        )

        if not response.text:
            raise ValueError("Gemini no devolvió respuesta")

        return response.text.strip()