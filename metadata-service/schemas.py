from datetime import datetime

from pydantic import BaseModel


class CADChangeBase(BaseModel):
    filename: str
    commit_sha: str
    pr_number: int
    entity_counts: dict[str, int] = {}
    layers: list[str] = []
    width: float = 0.0
    height: float = 0.0
    is_valid: bool = False
    validation_errors: list[str] = []

class CADChangeCreate(CADChangeBase):
    pass

class CADChangeUpdateScore(BaseModel):
    ai_risk_score: float
    ai_summary: str
    is_anomalous: bool

class CADChange(CADChangeBase):
    id: int
    ai_risk_score: float | None = None
    ai_summary: str | None = None
    is_anomalous: bool = False
    created_at: datetime

    class Config:
        orm_mode = True
