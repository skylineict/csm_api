from sqlmodel import SQLModel
from fast.main3 import engine

SQLModel.metadata.create_all(engine)
print("Database tables created/updated successfully!")