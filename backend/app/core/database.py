import logging
import time
from typing import Generator, Dict, Any
from urllib.parse import urlparse
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from app.core.config import settings

logger = logging.getLogger(__name__)

db_url = settings.DATABASE_URL
active_engine_name = "sqlite"
db_connection_notes = ""

def _safe_url(raw_url: str) -> str:
    """Return a sanitized connection string with password masked."""
    try:
        parsed = urlparse(raw_url)
        if parsed.password:
            safe_netloc = f"{parsed.username}:****@{parsed.hostname}"
            if parsed.port:
                safe_netloc += f":{parsed.port}"
            return raw_url.replace(parsed.netloc, safe_netloc)
        return raw_url
    except Exception:
        return "configured-db-url"

if db_url.startswith("sqlite"):
    engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False}
    )
    active_engine_name = "sqlite"
    db_connection_notes = "Operating with local SQLite development database."
else:
    try:
        engine = create_engine(
            db_url,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20
        )
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        active_engine_name = "postgresql"
        db_connection_notes = "Connected to production PostgreSQL server."
        logger.info(f"Connected to primary database: {_safe_url(db_url)}")
    except Exception as exc:
        active_engine_name = "sqlite_fallback"
        safe_configured = _safe_url(db_url)
        db_connection_notes = (
            f"PostgreSQL connection to {safe_configured} was not accessible ({exc.__class__.__name__}). "
            "Using local SQLite database (masteryloop.db). To switch to PostgreSQL, configure valid credentials in .env."
        )
        logger.warning(db_connection_notes)
        engine = create_engine(
            "sqlite:///./masteryloop.db",
            connect_args={"check_same_thread": False}
        )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_db_health() -> Dict[str, Any]:
    """Execute a lightweight probe to verify database connectivity and latency."""
    start = time.perf_counter()
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        latency_ms = round((time.perf_counter() - start) * 1000, 2)
        return {
            "status": "healthy",
            "dialect": engine.dialect.name,
            "engine_mode": active_engine_name,
            "latency_ms": latency_ms,
            "notes": db_connection_notes
        }
    except Exception as exc:
        return {
            "status": "degraded",
            "dialect": engine.dialect.name,
            "engine_mode": active_engine_name,
            "error": str(exc),
            "notes": db_connection_notes
        }


def init_db():
    """Create all tables defined in models if they do not exist."""
    import app.models  # Ensure all model tables are registered
    Base.metadata.create_all(bind=engine)
    logger.info("Database schemas initialized.")
