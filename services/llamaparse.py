import os
import json
import time

import asyncio
import httpx

LLAMA_PARSE_UPLOAD_URL = "https://api.cloud.llamaindex.ai/api/v2/parse/upload"
LLAMA_PARSE_RESULT_URL = "https://api.cloud.llamaindex.ai/api/v2/parse/{job_id}"

async def parse_file(context: dict):
    api_key = os.getenv("LLAMAINDEX_API_KEY")

    if not api_key:
        raise ValueError("LLAMAINDEX_API_KEY env variable was not found.")
    
    file_name = context["file_name"]
    file_bytes = context["file_bytes"]
    
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    configuration = {
        "tier": "agentic",
        "version": "latest",
        "input_options": {
            "pdf": {}
        },
        "output_options": {
            "markdown": {
                "annotate_links": True,
                "tables": {
                    "merge_continued_tables": True
                }
            }
        }
    }

    files = {
        "file": (file_name, file_bytes, "application/pdf"),
        "configuration": (None, json.dumps(configuration), "application/json"),
    }
    
    async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
        upload_response = await client.post(
            LLAMA_PARSE_UPLOAD_URL,
            headers=headers,
            files=files
        )

    if upload_response.status_code >= 400:
        raise Exception("There was an error sending the PDF to LlamaParse.")
    
    upload_data = upload_response.json()
    job = upload_data.get("job", {})
    job_id = job.get("id") or upload_data.get("id")

    if not job_id:
        raise Exception("job_id was not found in the parse job.")
    
    max_attempts = 30
    delay_seconds = 2

    async with httpx.AsyncClient(timeout=120.0, verify=False) as client:
        for _ in range(max_attempts):
            result_response = await client.get(
                LLAMA_PARSE_RESULT_URL.format(job_id=job_id),
                headers=headers,
                params={"expand": "markdown,text,items"}
            )

            if result_response.status_code >= 400:
                try:
                    error_body = result_response.json()
                except Exception:
                    error_body = result_response.text

                raise Exception(
                    f"There was an error getting the response from the parsing job. "
                    f"status={result_response.status_code}, body={error_body}"
                )
            
            result_data = result_response.json()
            status = result_data.get("job", {}).get("status")

            if status == "COMPLETED":
                context["markdown"] = result_data.get("markdown")

                return context
            
            if status in {"FAILED", "CANCELLED"}:
                raise Exception("Parse job ended with an error.")
            
            await asyncio.sleep(delay_seconds)

        raise Exception("The file took too long to process.")