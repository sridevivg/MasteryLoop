from fastapi import APIRouter
from app.core.database import check_db_health
from app.core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def get_health():
    db_health = check_db_health()
    return {
        "status": "healthy" if db_health.get("status") == "healthy" else "degraded",
        "service": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT,
        "database": db_health,
        "features": {
            "knowledge_tracing": "ready",
            "adaptive_assessment": "ready",
            "item_lifecycle": "ready",
            "event_bus": "active"
        }
    }
