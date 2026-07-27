import os
import time
import httpx
from celery_app import celery_app

VALIDATOR_URL = os.getenv("VALIDATOR_URL", "http://localhost:8001")
CONVERTER_URL = os.getenv("CONVERTER_URL", "http://localhost:8002")
METADATA_URL = os.getenv("METADATA_URL", "http://localhost:8003")
AI_AGENT_URL = os.getenv("AI_AGENT_URL", "http://localhost:8004")

@celery_app.task(name="tasks.process_github_webhook")
def process_github_webhook(pr_number: int, commit_sha: str, filename: str):
    """
    Orchestrates the entire CADFlow pipeline asynchronously.
    """
    # 1. Download the CAD file from GitHub (Mocked for this demo: we assume it's mounted or available)
    # In a real scenario, use GitHub API to download the raw blob.
    # For now, we will assume a file exists at /shared_data/sample.dxf
    filepath = f"/shared_data/{filename}"
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}. Mocking success for demo pipeline.")
        return {"status": "mock_success"}

    print(f"Starting pipeline for {filename} (PR #{pr_number})")

    # 2. Validate CAD File
    with open(filepath, 'rb') as f:
        val_response = httpx.post(f"{VALIDATOR_URL}/validate", files={"file": (filename, f, "application/dxf")})
    val_data = val_response.json()
    print("Validation Results:", val_data)

    # 3. Create Metadata Record
    create_data = {
        "filename": filename,
        "commit_sha": commit_sha,
        "pr_number": pr_number,
        "entity_counts": val_data.get("metadata", {}).get("entity_counts", {}),
        "layers": val_data.get("metadata", {}).get("layers", []),
        "width": val_data.get("metadata", {}).get("width", 0),
        "height": val_data.get("metadata", {}).get("height", 0),
        "is_valid": val_data.get("is_valid", False),
        "validation_errors": val_data.get("errors", [])
    }
    
    meta_response = httpx.post(f"{METADATA_URL}/changes/", json=create_data)
    change_record = meta_response.json()
    change_id = change_record["id"]
    print("Metadata Created, ID:", change_id)

    # 4. Get previous version for diffing
    history_response = httpx.get(f"{METADATA_URL}/changes/history/{filename}")
    history = history_response.json()
    
    old_metadata = {}
    if len(history) > 1:
        # history is ordered by created_at desc, so [1] is the previous
        old_meta_record = history[1]
        old_metadata = {
            "entity_counts": old_meta_record.get("entity_counts", {}),
            "width": old_meta_record.get("width", 0),
            "height": old_meta_record.get("height", 0)
        }
    
    # 5. AI Analysis (Diffing & Risk Scoring)
    analysis_req = {
        "old_metadata": old_metadata,
        "new_metadata": val_data.get("metadata", {}),
        "filename": filename
    }
    ai_response = httpx.post(f"{AI_AGENT_URL}/analyze", json=analysis_req)
    ai_data = ai_response.json()
    print("AI Analysis:", ai_data)
    
    # 6. Update Metadata with AI Score
    update_data = {
        "ai_risk_score": ai_data["risk_score"],
        "ai_summary": ai_data["summary"],
        "is_anomalous": ai_data["is_anomalous"]
    }
    httpx.put(f"{METADATA_URL}/changes/{change_id}/score", json=update_data)
    
    # 7. Post PR Comment via GitHub API (Mocked for demo)
    comment = f"""### CADFlow Review :robot:
**Status**: {"✅ Passed Validation" if val_data.get('is_valid') else "❌ Failed Validation"}
**Risk Score**: {ai_data['risk_score']:.2f}
**Anomaly Detected**: {"Yes ⚠️" if ai_data['is_anomalous'] else "No"}

**AI Summary**:
{ai_data['summary']}
"""
    print("Would post to GitHub PR:")
    print(comment)

    return {"status": "success", "change_id": change_id}
