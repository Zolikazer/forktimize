import os

from fastapi import FastAPI
from sqlmodel import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from database.data_access import is_database_empty
from database.db import init_db, engine
from error_handling.exceptions import MealPlanRequestException
from jobs.job_scheduler import scheduler, run_fetch_job
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
    os.makedirs(SETTINGS.LOG_DIR, exist_ok=True)
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)

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
