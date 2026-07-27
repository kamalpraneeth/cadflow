from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import ezdxf
import os

router = APIRouter(prefix="/converter", tags=["converter"])

@router.post("/geometry")
async def extract_geometry(file: UploadFile = File(...)):
    """
    Extracts raw 2D/3D coordinate geometry for the 3D viewer.
    """
    if not file.filename.endswith('.dxf'):
        raise HTTPException(status_code=400, detail="Only DXF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        doc = ezdxf.readfile(tmp_path)
        msp = doc.modelspace()
        
        lines = []
        circles = []

        for entity in msp:
            if entity.dxftype() == 'LINE':
                lines.append({
                    "start": [entity.dxf.start.x, entity.dxf.start.y, entity.dxf.start.z],
                    "end": [entity.dxf.end.x, entity.dxf.end.y, entity.dxf.end.z]
                })
            elif entity.dxftype() == 'CIRCLE':
                circles.append({
                    "center": [entity.dxf.center.x, entity.dxf.center.y, entity.dxf.center.z],
                    "radius": entity.dxf.radius
                })

        return JSONResponse({"lines": lines, "circles": circles})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
