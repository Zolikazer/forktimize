import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from database.db import init_db
from jobs.job_scheduler import scheduler
from monitoring.logger import LoggingMiddleware, LOGGER
from routers.planner_routes import planner

app = FastAPI()
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
    LOGGER.info("🚀 Starting up...")
    LOGGER.info(f"🔧 Environment: {os.getenv('ENV', 'development')}")
    init_db()
    LOGGER.info("🌐 Database initialized.")
    scheduler.start()
    LOGGER.info("Jobs scheduled.")


@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    LOGGER.info("Jobs stopped.")