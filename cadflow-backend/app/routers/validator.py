import os
import tempfile

import ezdxf
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/validator", tags=["validator"])

MIN_WALL_THICKNESS = 0.1

@router.post("/validate")
async def validate_dxf(file: UploadFile = File(...)):
    if not file.filename.endswith('.dxf'):
        raise HTTPException(status_code=400, detail="Only DXF files are supported")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        doc = ezdxf.readfile(tmp_path)
        msp = doc.modelspace()
        
        errors = []
        entity_counts = {}
        layers = set()
        
        min_x, min_y = float('inf'), float('inf')
        max_x, max_y = float('-inf'), float('-inf')

        for entity in msp:
            etype = entity.dxftype()
            entity_counts[etype] = entity_counts.get(etype, 0) + 1
            layers.add(entity.dxf.layer)
            
            # Simple bounding box extraction (for lines)
            if etype == 'LINE':
                start, end = entity.dxf.start, entity.dxf.end
                min_x = min(min_x, start.x, end.x)
                max_x = max(max_x, start.x, end.x)
                min_y = min(min_y, start.y, end.y)
                max_y = max(max_y, start.y, end.y)
                
                # Tolerance check
                length = ((end.x - start.x)**2 + (end.y - start.y)**2)**0.5
                if length < MIN_WALL_THICKNESS:
                    errors.append(f"Line entity too short ({length:.4f} < {MIN_WALL_THICKNESS}). Possible micro-geometry.")

        metadata = {
            "entity_counts": entity_counts,
            "layers": list(layers),
        }
        
        if min_x != float('inf'):
            metadata.update({
                "min_x": min_x, "max_x": max_x,
                "min_y": min_y, "max_y": max_y,
                "width": max_x - min_x,
                "height": max_y - min_y
            })

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "metadata": metadata
        }
    except Exception as e:
        return {"is_valid": False, "errors": [f"File parsing error: {e!s}"], "metadata": {}}
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
