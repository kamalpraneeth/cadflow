import ezdxf
import os

def create_sample_dxf(filename):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    doc.layers.add("OUTLINE", color=2)
    doc.layers.add("HOLES", color=1)
    
    msp.add_lwpolyline([(0, 0), (10, 0), (10, 10), (0, 10)], close=True, dxfattribs={'layer': 'OUTLINE'})
    msp.add_circle((2, 2), radius=1.0, dxfattribs={'layer': 'HOLES'})
    msp.add_circle((8, 8), radius=1.0, dxfattribs={'layer': 'HOLES'})
    msp.add_line((5, 5), (5, 5.05), dxfattribs={'layer': 'OUTLINE'})
    
    doc.saveas(filename)

if __name__ == "__main__":
    os.makedirs("shared_data", exist_ok=True)
    create_sample_dxf("shared_data/sample.dxf")
    create_sample_dxf("shared_data/sample_v2.dxf")
    print("Mock DXF files generated successfully in shared_data/")
