import os

from fastapi import FastAPI
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from database.data_access import is_database_empty
from database.db import init_db, ENGINE
from exceptions import MealPlanRequestException
from jobs.food_data_collector_job import run_collect_food_data_job
from jobs.database_backup_job import run_database_backup_job
from jobs.job_scheduler import SCHEDULER
from monitoring.logging import LoggingMiddleware, APP_LOGGER
from routers.meal_planner import meal_planner
from settings import SETTINGS

app = FastAPI(root_path="/api")
app.include_router(meal_planner)
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(MealPlanRequestException)
async def meal_plan_exception_handler(_: Request, exc: MealPlanRequestException):
    return JSONResponse(
        status_code=422,
        content={
            "code": exc.error_code,
            "message": exc.message
        }
    )


@app.on_event("startup")
def on_startup():
    with Session(ENGINE) as session:
        APP_LOGGER.info("🚀 Starting up...")
        APP_LOGGER.info(f"🔧 Environment: {os.getenv('ENV', 'development')} mode: {SETTINGS.MODE.name}")

        try:
            init_db()
            APP_LOGGER.info("🌐 Database initialized.")

            SCHEDULER.add_job(run_collect_food_data_job, "cron", hour=0, minute=0)
            SCHEDULER.add_job(run_database_backup_job, "cron", hour=22, minute=0)
            APP_LOGGER.info("Jobs scheduled.")

            if is_database_empty(session):
                APP_LOGGER.info("🔄 Cold start detected. Running initial fetch job...")
                SCHEDULER.add_job(run_collect_food_data_job, "date")

            SCHEDULER.start()
        except Exception as e:
            APP_LOGGER.error(f"Something fucked when starting upp the app {e}")


@app.on_event("shutdown")
def shutdown_event():
    SCHEDULER.shutdown()
    APP_LOGGER.info("Jobs stopped.")
