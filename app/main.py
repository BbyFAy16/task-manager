from fastapi import FastAPI

from .database import Base, engine
from .routers import auth, projects, tasks

# Convenient for local dev / first run; in staging/production, use
# `alembic upgrade head` (see alembic/) instead of relying on this.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Management API",
    description="A FastAPI backend for multi-user, multi-project task management with role-based access control.",
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(tasks.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}
