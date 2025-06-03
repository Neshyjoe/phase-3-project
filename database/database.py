


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///health_simplified.db")

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_session():
    session = SessionLocal()
    return session