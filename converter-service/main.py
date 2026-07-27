from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse, Response
import shutil
import os

from core.converter import convert_dxf_to_json, convert_dxf_to_svg

app = FastAPI(title="CADFlow Converter Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/convert/json")
async def convert_to_json(file: UploadFile = File(...)):
    if not file.filename.endswith(".dxf"):
        raise HTTPException(status_code=400, detail="Only .dxf files are supported")
    
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        json_data = convert_dxf_to_json(temp_path)
    except Exception as e:
        os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")
        
    os.remove(temp_path)
    return JSONResponse(content=json_data)

@app.post("/convert/svg")
async def convert_to_svg(file: UploadFile = File(...)):
    if not file.filename.endswith(".dxf"):
        raise HTTPException(status_code=400, detail="Only .dxf files are supported")
    
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        svg_content = convert_dxf_to_svg(temp_path)
    except Exception as e:
        os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error converting file: {str(e)}")
        
    os.remove(temp_path)
    return Response(content=svg_content, media_type="image/svg+xml")
