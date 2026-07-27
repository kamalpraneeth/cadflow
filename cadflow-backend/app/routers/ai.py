import numpy as np
from app.core.llm_client import generate_cad_summary
from app.database.models import CADChange
from app.database.session import get_db
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sklearn.ensemble import IsolationForest
from sqlalchemy.orm import Session

router = APIRouter(prefix="/ai", tags=["ai"])

class AnalyzeRequest(BaseModel):
    change_id: int
    filename: str
    new_metadata: dict

# Mock historical data for IsolationForest
MOCK_HISTORICAL_FEATURES = np.array([
    [10, 5, 5, 2], [12, 6, 6, 2], [9, 5, 4, 1], [11, 5, 5, 2], [100, 50, 50, 20] # The last one is an anomaly
])
model = IsolationForest(contamination=0.1, random_state=42)
model.fit(MOCK_HISTORICAL_FEATURES)

def extract_features(meta: dict) -> list:
    counts = meta.get("entity_counts", {})
    return [
        counts.get("LINE", 0) + counts.get("LWPOLYLINE", 0),
        counts.get("CIRCLE", 0) + counts.get("ARC", 0),
        meta.get("width", 0.0),
        meta.get("height", 0.0)
    ]

@router.post("/analyze")
def analyze_cad_change(request: AnalyzeRequest, db: Session = Depends(get_db)):
    # 1. Fetch previous metadata for comparison
    previous_change = db.query(CADChange).filter(
        CADChange.filename == request.filename,
        CADChange.id < request.change_id
    ).order_by(CADChange.id.desc()).first()
    
    old_meta = previous_change.extracted_metadata if previous_change else {}
    
    # 2. AI Summarization (Groq)
    summary = generate_cad_summary(old_meta, request.new_metadata, request.filename)
    
    # 3. Anomaly Detection (IsolationForest)
    features = extract_features(request.new_metadata)
    score = float(model.decision_function([features])[0])
    # Lower score = more anomalous
    is_anomalous = bool(score < 0)
    
    # Scale risk score between 0 and 1
    risk_score = 1.0 - (1.0 / (1.0 + np.exp(-score)))
    
    return {
        "summary": summary,
        "is_anomalous": is_anomalous,
        "risk_score": risk_score
    }
