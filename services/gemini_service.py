import os
import json

from google import genai
from google.genai import types

from utils import get_gemini_extract_data_prompt, SCHEMA_EXTRACT_DATA

async def extraer_datos(context: dict) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY.")
    
    client = genai.Client(api_key=api_key)
    model = "gemini-3-flash-preview"

    markdown_cv = context.get("markdown")
    prompt = get_gemini_extract_data_prompt(markdown_cv)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            response_mime_type="application/json",
            response_json_schema=SCHEMA_EXTRACT_DATA
        )
    )

    if not response.text:
        raise ValueError("Gemini no devolvió respuesta")
    
    try:
        extracted_data = json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini devolvió un JSON inválido: {e}")

    context["cv_data"] = extracted_data
    return context