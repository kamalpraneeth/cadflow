from fastapi import APIRouter, Request
from app.tasks import process_github_webhook

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/github")
async def github_webhook(request: Request):
    payload = await request.json()
    
    # In a real app, you'd extract the PR number, commit SHA, and download the changed CAD file.
    # For this portfolio demo, we'll extract standard fields and trigger the pipeline.
    
    pr_number = payload.get("pull_request", {}).get("number", 0)
    commit_sha = payload.get("pull_request", {}).get("head", {}).get("sha", "unknown")
    
    # Mocking the file download (in reality, you'd fetch from GitHub API)
    # The worker task will handle generating the mock DXF for the pipeline.
    task = process_github_webhook.delay(pr_number, commit_sha, "sample.dxf")
    
    return {"status": "accepted", "message": f"Pipeline triggered for PR {pr_number}"}
