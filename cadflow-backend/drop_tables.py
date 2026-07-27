from app.database.session import engine
from app.database import models

print("Dropping tables...")
models.Base.metadata.drop_all(bind=engine)
print("Creating tables...")
models.Base.metadata.create_all(bind=engine)
print("Done!")
