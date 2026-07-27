from sqlalchemy import Column, Integer, String, Float, Boolean, JSON, DateTime
from sqlalchemy.sql import func
from database import Base

class CADChange(Base):
    __tablename__ = "cad_changes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    commit_sha = Column(String, index=True)
    pr_number = Column(Integer, index=True)
    
    # Metadata extracted from Validator
    entity_counts = Column(JSON, default={})
    layers = Column(JSON, default=[])
    width = Column(Float, default=0.0)
    height = Column(Float, default=0.0)
    
    # Validation results
    is_valid = Column(Boolean, default=False)
    validation_errors = Column(JSON, default=[])
    
    # AI Risk Score
    ai_risk_score = Column(Float, nullable=True)
    ai_summary = Column(String, nullable=True)
    
    # Anomaly Detection Flag
    is_anomalous = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
