from fastapi import FastAPI
from api.test import router as gemini_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app = FastAPI()

app.include_router(gemini_router, prefix="/api")