import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.database import SessionLocal
from app.services.job_collector import scan_due_sources

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self) -> None:
        self.scheduler = BackgroundScheduler(timezone="UTC")

    def start(self) -> None:
        if self.scheduler.running:
            return
        self.scheduler.add_job(self.run_scan, "interval", minutes=1, id="job-source-scanner")
        self.scheduler.start()
        logger.info("Background scheduler started")

    def shutdown(self) -> None:
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)

    def run_scan(self) -> None:
        db = SessionLocal()
        try:
            results = scan_due_sources(db)
            if results:
                logger.info("Scanned job sources: %s", results)
        except Exception:
            logger.exception("Scheduled job source scan failed")
        finally:
            db.close()
