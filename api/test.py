from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from gemini_service import GeminiService

router = APIRouter()

class TestRequest(BaseModel):
    prompt: str

@router.post("/test-gemini")
def test_gemini(request: TestRequest):
    try:
        gemini = GeminiService()

        response = gemini.test_prompt(request.prompt)

        return {
            "success": True,
            "prompt": request.prompt,
            "response": response
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))