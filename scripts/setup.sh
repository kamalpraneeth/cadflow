#!/bin/bash
set -e

echo "Setting up CADFlow environment..."

# 1. Create shared_data directory
mkdir -p shared_data

# 2. Setup a virtual environment to generate mock DXF
echo "Creating temporary virtual environment to generate test DXF..."
python -m venv venv
# Note: This runs in bash, so activate script depends on OS, but we can just use the explicit path.
# Since this script might run on Ubuntu (GitHub Actions) or locally (Git Bash/WSL), we handle paths:
if [ -f "venv/Scripts/python" ]; then
    PYTHON="venv/Scripts/python"
    PIP="venv/Scripts/pip"
else
    PYTHON="venv/bin/python"
    PIP="venv/bin/pip"
fi

$PIP install ezdxf

# Generate a mock DXF file
cat << 'EOF' > generate_mock_dxf.py
import ezdxf

def create_sample_dxf(filename):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    
    # Add some layers
    doc.layers.add("OUTLINE", color=2)
    doc.layers.add("HOLES", color=1)
    
    # Draw an outline (square)
    msp.add_lwpolyline([(0, 0), (10, 0), (10, 10), (0, 10)], close=True, dxfattribs={'layer': 'OUTLINE'})
    
    # Draw some holes (circles)
    msp.add_circle((2, 2), radius=1.0, dxfattribs={'layer': 'HOLES'})
    msp.add_circle((8, 8), radius=1.0, dxfattribs={'layer': 'HOLES'})
    
    # Draw a line that might trigger the minimum length tolerance
    msp.add_line((5, 5), (5, 5.05), dxfattribs={'layer': 'OUTLINE'})
    
    doc.saveas(filename)

if __name__ == "__main__":
    create_sample_dxf("shared_data/sample.dxf")
    create_sample_dxf("shared_data/sample_v2.dxf")
EOF

$PYTHON generate_mock_dxf.py
echo "Mock DXF files generated in shared_data/"

# Clean up
rm generate_mock_dxf.py
# Don't delete venv, it might be used for tests later

echo "Setup complete. You can now run: bash scripts/run_all.sh"
