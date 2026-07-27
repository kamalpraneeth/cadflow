from app.tasks import process_github_webhook
from fastapi import APIRouter, BackgroundTasks, Request

router = APIRouter(prefix="/webhook", tags=["webhook"])

@router.post("/github")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    # In a real app, you'd extract the PR number, commit SHA, and download the changed CAD file.
    # For this portfolio demo, we'll extract standard fields and trigger the pipeline.
    
    pr_number = payload.get("pull_request", {}).get("number", 0)
    commit_sha = payload.get("pull_request", {}).get("head", {}).get("sha", "unknown")
    
    # Run the processing pipeline as a FastAPI Background Task instead of Celery
    background_tasks.add_task(process_github_webhook, pr_number, commit_sha, "sample.dxf")
    
    return {"status": "accepted", "message": f"Pipeline triggered for PR {pr_number}"}
