from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import Config

# Create database engine
engine = create_engine(Config.DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """
    Yields a database session and ensures it is properly closed.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
