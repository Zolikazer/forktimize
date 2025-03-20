import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.db import init_db
from jobs.job_scheduler import scheduler, is_database_empty, run_fetch_job
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
    APP_LOGGER.info("🚀 Starting up...")
    APP_LOGGER.info(f"🔧 Environment: {os.getenv('ENV', 'development')}")

    init_db()
    APP_LOGGER.info("🌐 Database initialized.")

    scheduler.add_job(run_fetch_job, "cron", hour=0, minute=0)
    APP_LOGGER.info("Jobs scheduled.")

    if is_database_empty():
        APP_LOGGER.info("🔄 Cold start detected. Running initial fetch job...")
        scheduler.add_job(run_fetch_job, "date")

    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    APP_LOGGER.info("Jobs stopped.")
