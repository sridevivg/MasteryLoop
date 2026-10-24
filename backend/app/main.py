import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, check_db_health
from app.api.health import router as health_router
from app.api.auth import router as auth_router
from app.api.curriculum import router as curriculum_router
from app.api.sessions import router as sessions_router
from app.api.mastery import router as mastery_router
from app.api.tutor import router as tutor_router
from app.api.items import router as items_router
from app.api.coding import router as coding_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("masteryloop")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database schema is initialized and seeded
    logger.info(f"Starting {settings.PROJECT_NAME} backend in {settings.ENVIRONMENT} mode...")
    init_db()
    db_status = check_db_health()
    logger.info(f"Database status: {db_status}")

    try:
        from app.seed.curriculum_seed import seed_curriculum
        from app.seed.question_seed import seed_questions
        from app.seed.rag_seed import seed_rag_knowledge
        from app.seed.user_seed import seed_demo_users
        from app.core.database import SessionLocal
        with SessionLocal() as db_session:
            seed_curriculum(db_session)
            seed_questions(db_session)
            seed_rag_knowledge(db_session)
            seed_demo_users(db_session)
        logger.info("Auto-seeded curriculum, question bank, Qdrant knowledge base, and demo users.")
    except Exception as e:
        logger.warning(f"Startup seeding notice: {e}")

    yield
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME} backend.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Knowledge-Tracing-Driven Adaptive Assessment, Psychometrically-Validated AI Item Generation, and Learning Intelligence Platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for Vite frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root-level health probe
@app.get("/health", tags=["Health"])
def root_health():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "database": check_db_health()
    }


# Include API routers under /api/v1
app.include_router(health_router, prefix=settings.API_V1_STR)
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(curriculum_router, prefix=settings.API_V1_STR)
app.include_router(sessions_router, prefix=settings.API_V1_STR)
app.include_router(mastery_router, prefix=settings.API_V1_STR)
app.include_router(tutor_router, prefix=settings.API_V1_STR)
app.include_router(items_router, prefix=settings.API_V1_STR)
app.include_router(coding_router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
