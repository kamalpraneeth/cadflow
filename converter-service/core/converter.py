import io
from typing import Any

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext
from ezdxf.addons.drawing.svg import SVGBackend


def convert_dxf_to_json(filepath: str) -> dict[str, Any]:
    """
    Converts core DXF entities into a structured JSON payload for web rendering or diffing.
    """
    doc = ezdxf.readfile(filepath)
    msp = doc.modelspace()
    
    entities = []
    for entity in msp:
        entity_dict = {"type": entity.dxftype()}
        if entity.dxftype() == 'LINE':
            entity_dict["start"] = {"x": entity.dxf.start.x, "y": entity.dxf.start.y}
            entity_dict["end"] = {"x": entity.dxf.end.x, "y": entity.dxf.end.y}
        elif entity.dxftype() == 'CIRCLE':
            entity_dict["center"] = {"x": entity.dxf.center.x, "y": entity.dxf.center.y}
            entity_dict["radius"] = entity.dxf.radius
        elif entity.dxftype() == 'LWPOLYLINE':
            points = [{"x": p[0], "y": p[1]} for p in entity.get_points(format="xy")]
            entity_dict["points"] = points
            
        entities.append(entity_dict)
        
    return {"entities": entities, "count": len(entities)}

def convert_dxf_to_svg(filepath: str) -> str:
    """
    Converts a DXF file to an SVG string for visual previews.
    """
    doc = ezdxf.readfile(filepath)
    msp = doc.modelspace()
    
    # We use ezdxf's drawing addon to render to SVG
    fig = io.StringIO()
    ctx = RenderContext(doc)
    backend = SVGBackend(ctx.current_layout_properties)
    frontend = Frontend(ctx, backend)
    
    frontend.draw_layout(msp, finalize=True)
    
    # The SVG string
    svg_string = backend.get_string(
        page=(0, 0, 1000, 1000) # Optional explicit viewbox/page settings
    )
    return svg_string
