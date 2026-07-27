from typing import Any

import ezdxf


def validate_dxf(filepath: str) -> tuple[bool, list[str], dict[str, Any]]:
    """
    Validates a DXF file for engineering tolerances and extracts metadata.
    Returns: (is_valid, list of errors, metadata dictionary)
    """
    errors = []
    metadata = {
        "entity_counts": {},
        "layers": [],
        "min_x": None,
        "max_x": None,
        "min_y": None,
        "max_y": None
    }
    
    try:
        doc = ezdxf.readfile(filepath)
    except OSError:
        errors.append("Not a valid DXF file or could not be read.")
        return False, errors, metadata
    except ezdxf.DXFStructureError as e:
        errors.append(f"Invalid or corrupted DXF structure: {e!s}")
        return False, errors, metadata

    msp = doc.modelspace()
    
    # 1. Extract Layers
    for layer in doc.layers:
        metadata["layers"].append(layer.dxf.name)
        
    # 2. Extract Entities and Metadata
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    
    for entity in msp:
        dxftype = entity.dxftype()
        metadata["entity_counts"][dxftype] = metadata["entity_counts"].get(dxftype, 0) + 1
        
        # Engineering Rule: Minimum Line length check (e.g., no micro-lines < 0.1 units)
        if dxftype == 'LINE':
            start = entity.dxf.start
            end = entity.dxf.end
            length = ((end.x - start.x)**2 + (end.y - start.y)**2)**0.5
            if length < 0.1:
                errors.append(f"Line entity too short ({length:.4f} < 0.1). Possible micro-geometry.")
                
            # Update bounds
            min_x = min(min_x, start.x, end.x)
            max_x = max(max_x, start.x, end.x)
            min_y = min(min_y, start.y, end.y)
            max_y = max(max_y, start.y, end.y)
            
        elif dxftype == 'CIRCLE':
            center = entity.dxf.center
            radius = entity.dxf.radius
            min_x = min(min_x, center.x - radius)
            max_x = max(max_x, center.x + radius)
            min_y = min(min_y, center.y - radius)
            max_y = max(max_y, center.y + radius)

    if min_x != float('inf'):
        metadata["min_x"] = min_x
        metadata["max_x"] = max_x
        metadata["min_y"] = min_y
        metadata["max_y"] = max_y
        metadata["width"] = max_x - min_x
        metadata["height"] = max_y - min_y
    else:
        metadata["min_x"] = 0
        metadata["max_x"] = 0
        metadata["min_y"] = 0
        metadata["max_y"] = 0
        metadata["width"] = 0
        metadata["height"] = 0

    is_valid = len(errors) == 0
    return is_valid, errors, metadata
