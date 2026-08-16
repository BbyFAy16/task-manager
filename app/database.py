import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Defaults to a local SQLite file for dev; set DATABASE_URL to a Postgres URL
# (e.g. postgresql://user:pass@localhost:5432/taskdb) for production.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./task_manager.db")

# check_same_thread is only needed for SQLite, which by default only allows
# the thread that created a connection to use it. FastAPI's TestClient and
# request handling can hit the same connection from different threads.
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a DB session and always closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
