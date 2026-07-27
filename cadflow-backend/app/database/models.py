import datetime

from sqlalchemy import JSON, Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CADChange(Base):
    __tablename__ = "cad_changes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    pr_number = Column(Integer, index=True)
    commit_sha = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Validation Domain
    is_valid = Column(Boolean, default=True)
    validation_errors = Column(JSON, nullable=True)
    
    # Converter/Metadata Domain
    extracted_metadata = Column(JSON, nullable=True)
    
    # AI/Anomaly Domain
    ai_risk_score = Column(Float, nullable=True)
    is_anomalous = Column(Boolean, default=False)
    ai_summary = Column(String, nullable=True)
