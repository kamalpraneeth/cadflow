from typing import Any

from core.anthropic_client import generate_cad_summary
from fastapi import FastAPI, HTTPException
from ml.anomaly_detector import detect_anomaly
from pydantic import BaseModel

app = FastAPI(title="CADFlow AI Agent Service")

class AnalysisRequest(BaseModel):
    old_metadata: dict[str, Any]
    new_metadata: dict[str, Any]
    filename: str

class AnalysisResponse(BaseModel):
    summary: str
    is_anomalous: bool
    risk_score: float

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_cad_change(request: AnalysisRequest):
    try:
        # 1. Generate Plain English Summary using Anthropic
        summary = generate_cad_summary(request.old_metadata, request.new_metadata, request.filename)
        
        # 2. Detect Anomalies using Scikit-Learn Isolation Forest
        is_anomalous, risk_score = detect_anomaly(request.old_metadata, request.new_metadata)
        
        return AnalysisResponse(
            summary=summary,
            is_anomalous=is_anomalous,
            risk_score=risk_score
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
