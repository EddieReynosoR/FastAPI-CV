import os
import json
from google import genai
from google.genai import types

from utils import get_gemini_career_path_prompt, SCHEMA_CAREER_PATH

async def generate_career_path(context: dict) -> dict:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY env variable was not found.")

    cv_data = context.get("cv_data")
    if not cv_data:
        raise ValueError("Extracted information of CV context['cv_data'] was not found.")

    client = genai.Client(api_key=api_key)
    model = "gemini-3-flash-preview"

    schema = SCHEMA_CAREER_PATH
    prompt = get_gemini_career_path_prompt(cv_data)

    response = await client.aio.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            response_mime_type="application/json",
            response_json_schema=schema,
        )
    )

    if not response.text:
        raise ValueError("Gemini did'nt return any response.")

    try:
        career_path_data = json.loads(response.text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Gemini returned an invalid JSON for the career path: {e}")

    context["career_path"] = career_path_data
    return context