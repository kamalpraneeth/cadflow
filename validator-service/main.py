import os
import shutil
from typing import Any

from core.validator import validate_dxf
from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

app = FastAPI(title="CADFlow Validator Service")

class ValidationResult(BaseModel):
    is_valid: bool
    errors: list[str]
    metadata: dict[str, Any]

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/validate", response_model=ValidationResult)
async def validate_file(file: UploadFile = File(...)):
    if not file.filename.endswith(".dxf"):
        raise HTTPException(status_code=400, detail="Only .dxf files are supported")
    
    # Save the file temporarily
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        is_valid, errors, metadata = validate_dxf(temp_path)
    except Exception as e:
        os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error processing file: {e!s}")
    
    os.remove(temp_path)
    
    return ValidationResult(
        is_valid=is_valid,
        errors=errors,
        metadata=metadata
    )
