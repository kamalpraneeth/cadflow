import os

import httpx
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI(title="CADFlow Dashboard")
templates = Jinja2Templates(directory="templates")

METADATA_URL = os.getenv("METADATA_URL", "http://localhost:8003")

@app.get("/")
async def dashboard(request: Request):
    try:
        response = httpx.get(f"{METADATA_URL}/changes/?limit=50")
        changes = response.json()
    except Exception as e:
        changes = []
        print(f"Error fetching metadata: {e}")
        
    return templates.TemplateResponse(request=request, name="index.html", context={"changes": changes})
