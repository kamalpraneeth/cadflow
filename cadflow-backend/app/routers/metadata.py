
from app.database.models import CADChange
from app.database.session import get_db
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

router = APIRouter(prefix="/metadata", tags=["metadata"])

class ChangeCreate(BaseModel):
    filename: str
    pr_number: int
    commit_sha: str
    is_valid: bool
    validation_errors: list = []
    extracted_metadata: dict = {}

class ScoreUpdate(BaseModel):
    ai_risk_score: float
    is_anomalous: bool
    ai_summary: str

@router.post("/changes/")
def create_change(change: ChangeCreate, db: Session = Depends(get_db)):
    db_change = CADChange(
        filename=change.filename,
        pr_number=change.pr_number,
        commit_sha=change.commit_sha,
        is_valid=change.is_valid,
        validation_errors=change.validation_errors,
        extracted_metadata=change.extracted_metadata
    )
    db.add(db_change)
    db.commit()
    db.refresh(db_change)
    return {"id": db_change.id}

@router.get("/changes/")
def get_changes(limit: int = 50, db: Session = Depends(get_db)):
    return db.query(CADChange).order_by(CADChange.id.desc()).limit(limit).all()

@router.get("/changes/history/{filename}")
def get_file_history(filename: str, db: Session = Depends(get_db)):
    return db.query(CADChange).filter(CADChange.filename == filename).order_by(CADChange.id.desc()).all()

@router.put("/changes/{change_id}/score")
def update_score(change_id: int, score_data: ScoreUpdate, db: Session = Depends(get_db)):
    change = db.query(CADChange).filter(CADChange.id == change_id).first()
    if not change:
        raise HTTPException(status_code=404, detail="Change not found")
    
    change.ai_risk_score = score_data.ai_risk_score
    change.is_anomalous = score_data.is_anomalous
    change.ai_summary = score_data.ai_summary
    
    db.commit()
    return {"status": "updated"}
