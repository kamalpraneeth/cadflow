import os
import tempfile

import ezdxf
import httpx
import logging

logger = logging.getLogger(__name__)

# Base URL for the monolith APIs. Can be overridden in production (e.g. internal Render URL)
API_BASE = os.getenv("API_BASE_URL", f"http://localhost:{os.getenv('PORT', '8000')}")

def generate_mock_dxf(filepath: str):
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    msp.add_lwpolyline([(1, 1), (9, 1), (9, 9), (1, 9)], close=True, dxfattribs={'layer': 'OUTLINE'})
    msp.add_circle((5, 5), radius=2, dxfattribs={'layer': 'HOLES'})
    msp.add_circle((2, 2), radius=0.5, dxfattribs={'layer': 'HOLES'})
    # msp.add_line((1, 1), (1, 1.05))  # Removed intentional micro-geometry that fails validation
    doc.saveas(filepath)

def process_github_webhook(pr_number: int, commit_sha: str, filename: str):
    logger.warning(f"Starting pipeline for {filename} (PR #{pr_number})")
    
    # 1. Download/Generate CAD File
    with tempfile.NamedTemporaryFile(suffix=".dxf", delete=False) as tmp:
        dxf_path = tmp.name
    try:
        generate_mock_dxf(dxf_path)
        
        # 2. Validation Service
        with open(dxf_path, 'rb') as f:
            val_resp = httpx.post(f"{API_BASE}/validator/validate", files={"file": f})
        val_resp.raise_for_status()
        val_data = val_resp.json()
        logger.warning(f"Validation Results:\n {val_data}")
        
        # 3. Metadata Service (Save)
        change_payload = {
            "filename": filename,
            "pr_number": pr_number,
            "commit_sha": commit_sha,
            "is_valid": val_data.get("is_valid", False),
            "validation_errors": val_data.get("errors", []),
            "extracted_metadata": val_data.get("metadata", {})
        }
        meta_resp = httpx.post(f"{API_BASE}/metadata/changes/", json=change_payload)
        meta_resp.raise_for_status()
        change_id = meta_resp.json()["id"]
        logger.warning(f"Metadata Created, ID:\n {change_id}")
        
        # 4. AI Analysis Service
        ai_payload = {
            "change_id": change_id,
            "filename": filename,
            "new_metadata": val_data.get("metadata", {})
        }
        ai_resp = httpx.post(f"{API_BASE}/ai/analyze", json=ai_payload)
        ai_resp.raise_for_status()
        ai_data = ai_resp.json()
        logger.warning(f"AI Analysis:\n {ai_data}")
        
        # 5. Update Metadata with AI Score
        score_payload = {
            "ai_risk_score": ai_data["risk_score"],
            "is_anomalous": ai_data["is_anomalous"],
            "ai_summary": ai_data["summary"]
        }
        httpx.put(f"{API_BASE}/metadata/changes/{change_id}/score", json=score_payload)
        
        # 6. Post Review Comment to GitHub PR (Mock)
        review_comment = f"""### CADFlow Review :robot:
**Status**: {'✅ Passed' if val_data['is_valid'] else '❌ Failed Validation'}
**Risk Score**: {ai_data['risk_score']:.2f}
**Anomaly Detected**: {'Yes ⚠️' if ai_data['is_anomalous'] else 'No'}

**AI Summary**:
{ai_data['summary']}"""
        logger.warning(f"Would post to GitHub PR:\n{review_comment}")
        
        return {"status": "success", "change_id": change_id}
        
    finally:
        if os.path.exists(dxf_path):
            os.remove(dxf_path)
