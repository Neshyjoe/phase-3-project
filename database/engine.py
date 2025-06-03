


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Define the database URL
DATABASE_URL = "sqlite:///health_simplified.db"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

# Session maker to handle DB transactions
SessionLocal = sessionmaker(bind=engine)