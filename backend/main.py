import os

from fastapi import FastAPI
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware

from database.db import init_db, engine
from jobs.job_scheduler import scheduler, run_fetch_job
from repository.forktimize_repository import is_database_empty
from monitoring.logging import LoggingMiddleware, APP_LOGGER
from routers.planner_routes import planner

app = FastAPI(root_path="/api")
app.add_middleware(LoggingMiddleware)
app.include_router(planner)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    with Session(engine) as session:
        APP_LOGGER.info("🚀 Starting up...")
        APP_LOGGER.info(f"🔧 Environment: {os.getenv('ENV', 'development')}")

        try:
            init_db()
            APP_LOGGER.info("🌐 Database initialized.")

            scheduler.add_job(run_fetch_job, "cron", hour=0, minute=0)
            APP_LOGGER.info("Jobs scheduled.")

            if is_database_empty(session):
                APP_LOGGER.info("🔄 Cold start detected. Running initial fetch job...")
                scheduler.add_job(run_fetch_job, "date")

            scheduler.start()
        except Exception as e:
            APP_LOGGER.error(f"Something fucked when starting upp the app {e}")


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    APP_LOGGER.info("Jobs stopped.")
