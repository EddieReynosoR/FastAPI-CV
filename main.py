from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

import json

from services.upload_pdf import process_file
from services.llamaparse import parse_file
from services.gemini_service import extract_data
from services.career_path import generate_career_path

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Temporal workaround, should not be available in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/api/analyze-cv")
async def analyze_cv(file: UploadFile):
    async def stream():
        context = {"file": file}

        steps = [
            ("file_received", process_file),
            ("parsing_pdf", parse_file),
            ("extracting_data", extract_data),
            ("generate_career_path", generate_career_path)
        ]

        try:
            yield f"data: {json.dumps({'type': 'start'})}\n\n"

            for step_name, step_fn in steps:
                context = await step_fn(context)

                yield f"data: {json.dumps({
                    'type': 'step',
                    'step': step_name,
                    'status': 'done'
                })}\n\n"

            yield f"data: {json.dumps({
                'type': 'result',
                'career_path': context.get("career_path")
            })}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({
                'type': 'error',
                'message': str(e)
            })}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")