
from fastapi import UploadFile

async def process_file(context: dict):
    file: UploadFile = context["file"]

    if file.content_type != "application/pdf":
        raise Exception("Only PDF files are permitted.")
    
    file_bytes = await file.read()

    if not file_bytes:
        raise Exception("The file was empty.")
    
    context["file_bytes"] = file_bytes
    context["file_name"] = file.filename

    return context