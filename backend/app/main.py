import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.config import get_settings
from app.database import SessionLocal
from app.routers import applications, auth, job_sources, jobs, profiles, qa_memory
from app.routers import settings as settings_router
from app.services.auth_service import bootstrap_admin
from app.workers.scheduler import SchedulerService


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    logging.basicConfig(level=settings.log_level)
    logger = logging.getLogger(__name__)
    scheduler: SchedulerService | None = None

    if settings.environment != "test":
        db = SessionLocal()
        try:
            bootstrap_admin(db, settings)
        except Exception:
            logger.exception("Admin bootstrap failed. Confirm migrations have been applied.")
        finally:
            db.close()

        scheduler = SchedulerService()
        scheduler.start()
        app.state.scheduler = scheduler

    yield

    if scheduler:
        scheduler.shutdown()


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    api_prefix = "/api"
    app.include_router(auth.router, prefix=api_prefix)
    app.include_router(profiles.router, prefix=api_prefix)
    app.include_router(job_sources.router, prefix=api_prefix)
    app.include_router(jobs.router, prefix=api_prefix)
    app.include_router(applications.router, prefix=api_prefix)
    app.include_router(qa_memory.router, prefix=api_prefix)
    app.include_router(settings_router.router, prefix=api_prefix)

    @app.get("/api/health", tags=["health"])
    def health() -> dict[str, str]:
        return {"status": "ok"}

    frontend_dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if frontend_dist.exists():
        assets_dir = frontend_dist / "assets"
        if assets_dir.exists():
            app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

        @app.get("/{full_path:path}", include_in_schema=False)
        def serve_frontend(full_path: str) -> FileResponse:
            target = frontend_dist / full_path
            if target.is_file():
                return FileResponse(target)
            return FileResponse(frontend_dist / "index.html")

    return app


app = create_app()
