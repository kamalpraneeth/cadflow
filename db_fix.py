from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = None
with open("cadflow-backend/.env", "r") as f:
    for line in f:
        if line.startswith("DATABASE_URL="):
            db_url = line.strip().split("=")[1].strip('"')

if not db_url:
    print("NO DATABASE URL")
    exit(1)

DATABASE_URL = db_url

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

import app.database.models as md

groq_key = None
with open("cadflow-backend/.env", "r") as f:
    for line in f:
        if line.startswith("GROQ_API_KEY="):
            groq_key = line.strip().split("=")[1].strip('"')

from app.core import config, llm_client

config.settings.groq_api_key = groq_key

changes = db.query(md.CADChange).order_by(md.CADChange.id.desc()).limit(3).all()
for c in changes:
    print(f"Fixing PR {c.pr_number}...")
    try:
        new_summary = llm_client.generate_cad_summary({}, c.extracted_metadata, c.filename)
        c.ai_summary = new_summary
        db.commit()
        print("Success!")
    except Exception as e:
        print(f"Failed: {e}")

db.close()
