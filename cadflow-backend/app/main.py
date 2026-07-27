from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import validator, converter, metadata, ai, webhook
from app.database.session import engine, get_db
from app.database import models
from fastapi import Depends


app = FastAPI(title="CADFlow Modular Monolith API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(validator.router)
app.include_router(converter.router)
app.include_router(metadata.router)
app.include_router(ai.router)
app.include_router(webhook.router)

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

# Mount the templates directory from the old dashboard folder (or we can copy it)
# Assuming you run this from the cadflow-backend directory, we'll go up one level to find dashboard/templates
import os
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../dashboard/templates"))
templates = Jinja2Templates(directory=template_dir)

@app.get("/", response_class=HTMLResponse)
def root(request: Request, db=Depends(get_db)):
    # Fetch changes to display in the dashboard
    changes = db.query(models.CADChange).order_by(models.CADChange.id.desc()).limit(50).all()
    return templates.TemplateResponse(request=request, name="index.html", context={"changes": changes})
