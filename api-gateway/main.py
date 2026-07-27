from fastapi import FastAPI, Request, HTTPException
import logging

from celery_app import celery_app
from tasks import process_github_webhook

app = FastAPI(title="CADFlow API Gateway")
logger = logging.getLogger(__name__)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/webhook/github")
async def github_webhook(request: Request):
    """
    Receives GitHub webhook events. We are interested in PRs that modify .dxf files.
    """
    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")
    
    # Very simplified payload parsing for demonstration
    if event == "pull_request":
        action = payload.get("action")
        if action in ["opened", "synchronize"]:
            pr_number = payload.get("number")
            commit_sha = payload.get("pull_request", {}).get("head", {}).get("sha")
            
            # In a real app, we'd fetch the list of changed files from GitHub API here.
            # For this demo, we assume a specific file changed and is passed in the payload or mock it.
            # We'll dispatch a celery task to handle the heavy lifting.
            
            # Mocking the filename for demo purposes
            filename = payload.get("filename", "sample.dxf")
            
            logger.info(f"Triggering pipeline for PR #{pr_number}, commit {commit_sha}, file {filename}")
            process_github_webhook.delay(pr_number, commit_sha, filename)
            
            return {"status": "accepted", "message": f"Pipeline triggered for PR {pr_number}"}
            
    return {"status": "ignored"}
