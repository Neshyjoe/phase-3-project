from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine("sqlite:///health.db")
Session = sessionmaker(bind=engine)

def init_db():
    Base = declarative_base()