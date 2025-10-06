from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker
from pathlib import Path
import os
from app.core.config import settings

# Ensure data directory exists - Fixed for Render
db_path = settings.database_url.replace("sqlite:///", "")
try:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    # Ensure the directory is writable
    if not os.access(Path(db_path).parent, os.W_OK):
        # Try alternative path for Render
        if settings.is_render:
            alt_path = "/opt/render/project/data"
            Path(alt_path).mkdir(parents=True, exist_ok=True)
            settings.database_url = f"sqlite:///{alt_path}/cc.db"
            db_path = settings.database_url.replace("sqlite:///", "")
except Exception as e:
    print(f"Warning: Could not create data directory: {e}")
    # Fallback to current directory
    settings.database_url = "sqlite:///cc.db"
    db_path = "cc.db"

# Create engine with SQLite-specific settings
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url, 
    connect_args=connect_args,
    pool_pre_ping=True
)

# Enable foreign key constraints for SQLite
if settings.database_url.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
