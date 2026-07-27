
import database
import models
import schemas
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

app = FastAPI(title="CADFlow Metadata Service")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/changes/", response_model=schemas.CADChange)
def create_change(change: schemas.CADChangeCreate, db: Session = Depends(database.get_db)):
    db_change = models.CADChange(**change.dict())
    db.add(db_change)
    db.commit()
    db.refresh(db_change)
    return db_change

@app.put("/changes/{change_id}/score", response_model=schemas.CADChange)
def update_score(change_id: int, score_data: schemas.CADChangeUpdateScore, db: Session = Depends(database.get_db)):
    db_change = db.query(models.CADChange).filter(models.CADChange.id == change_id).first()
    if not db_change:
        raise HTTPException(status_code=404, detail="Change not found")
        
    db_change.ai_risk_score = score_data.ai_risk_score
    db_change.ai_summary = score_data.ai_summary
    db_change.is_anomalous = score_data.is_anomalous
    
    db.commit()
    db.refresh(db_change)
    return db_change

@app.get("/changes/", response_model=list[schemas.CADChange])
def list_changes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return db.query(models.CADChange).order_by(models.CADChange.created_at.desc()).offset(skip).limit(limit).all()

@app.get("/changes/history/{filename}", response_model=list[schemas.CADChange])
def get_file_history(filename: str, db: Session = Depends(database.get_db)):
    return db.query(models.CADChange).filter(models.CADChange.filename == filename).order_by(models.CADChange.created_at.desc()).all()
