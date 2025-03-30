from datetime import datetime

from sqlmodel import Session

from database.db import init_db, engine
from jobs.food_providers.inter_city_food_provider import InterCityFoodProvider
from jobs.food_providers.food_provider import FoodProviderStrategy
from model.food import Food, FoodProvider
from model.job_run import JobRun, JobStatus
from monitoring.logging import JOB_LOGGER
from settings import SETTINGS

DATA_ENDPOINT = f"{SETTINGS.CITY_FOOD_API_URL}/{SETTINGS.CITY_FOOD_API_FOOD_PATH}"
CURRENT_WEEK = datetime.now().isocalendar()[1]
CURRENT_YEAR = datetime.now().year


def fetch_and_store_food_selection(session: Session, strategy: FoodProviderStrategy, weeks_to_fetch: int = 3):
    for week in range(CURRENT_WEEK, CURRENT_WEEK + weeks_to_fetch):
        try:
            foods = strategy.fetch_foods_for(CURRENT_YEAR, week)
            _save_food_to_db(session, foods, week)

            job_id = _track_job_run(session, week, CURRENT_YEAR, JobStatus.SUCCESS, strategy.get_name())
            JOB_LOGGER.info(
                f"✅ Job ID={job_id}: Successfully fetched & stored data for {strategy.get_name()} Week {week}.")
        except Exception as e:
            job_id = _track_job_run(session, week, CURRENT_YEAR, JobStatus.FAILURE, strategy.get_name())
            JOB_LOGGER.error(f"❌ Job ID={job_id}: Unexpected error: {e}")


def _save_food_to_db(session: Session, foods: list[Food], week: int):
    for food in foods:
        session.merge(food)

    session.commit()

    JOB_LOGGER.info(f"✅ Week {week} food selection stored in the database.")


def _track_job_run(session: Session, week: int, year: int, status: JobStatus, provider: FoodProvider) -> int:
    job_run = JobRun(week=week, year=year, status=status, timestamp=datetime.now(), food_provider=provider)
    session.add(job_run)
    session.commit()
    session.refresh(job_run)

    JOB_LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Week={week}, Year={year}, Status={status}")
    return job_run.id


if __name__ == "__main__":
    SETTINGS.DATA_DIR.mkdir(parents=True, exist_ok=True)

    init_db()
    with Session(engine) as session:
        fetch_and_store_food_selection(session, InterCityFoodProvider(
            f"{SETTINGS.CITY_FOOD_API_URL}/{SETTINGS.CITY_FOOD_API_FOOD_PATH}", FoodProvider.CITY_FOOD))
