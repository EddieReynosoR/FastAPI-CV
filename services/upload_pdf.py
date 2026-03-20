
from fastapi import UploadFile, File, HTTPException

async def process_file(context: dict):
    file: UploadFile = context["file"]

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Solo se permiten archivos PDF.",
        )
    
    file_bytes = await file.read()

    if not file_bytes:
        raise HTTPException(
            status_code=400,
            detail="El archivo está vacío.",
        )
    
    context["file_bytes"] = file_bytes
    context["file_name"] = file.filename

    return context