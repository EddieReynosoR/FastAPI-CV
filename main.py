from fastapi import FastAPI, UploadFile
from fastapi.responses import StreamingResponse

import json

from services.upload_pdf import process_file
from services.llamaparse import parse_file
from services.gemini_service import extraer_datos
from services.career_path import generar_career_path

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "ok"}

@app.post("/api/analyze-cv")
async def analyze_cv(file: UploadFile):
    async def stream():
        context = {"file": file}

        steps = [
            ("archivo_recibido", process_file),
            ("parseando_pdf", parse_file),
            ("extrayendo_datos", extraer_datos),
            ("generar_career_path", generar_career_path)
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