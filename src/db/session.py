import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# create SQLAlchemy engine (for PostgreSQL)
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# create a configured "Session" class
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

# create a Base class for the models to inherit
Base = declarative_base()

# dependency that will be used in FastAPI endpoints to get the session
def get_db():
    """Dependency that yields a new database session for each request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()