from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime

class CADChangeBase(BaseModel):
    filename: str
    commit_sha: str
    pr_number: int
    entity_counts: Dict[str, int] = {}
    layers: List[str] = []
    width: float = 0.0
    height: float = 0.0
    is_valid: bool = False
    validation_errors: List[str] = []

class CADChangeCreate(CADChangeBase):
    pass

class CADChangeUpdateScore(BaseModel):
    ai_risk_score: float
    ai_summary: str
    is_anomalous: bool

class CADChange(CADChangeBase):
    id: int
    ai_risk_score: Optional[float] = None
    ai_summary: Optional[str] = None
    is_anomalous: bool = False
    created_at: datetime

    class Config:
        orm_mode = True
