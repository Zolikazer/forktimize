from datetime import datetime

from sqlmodel import Session

from database.db import init_db, engine
from jobs.food_providers.city_food_strategy import CityFoodStrategy
from jobs.food_providers.food_provider_strategy import FoodProviderStrategy
from model.food_providers import FoodProvider
from jobs.food_providers.inter_food_strategy import InterFoodStrategy
from jobs.serialization import save_to_json
from model.food import Food
from model.job_run import JobRun, JobStatus
from monitoring.logging import JOB_LOGGER
from settings import SETTINGS

CURRENT_WEEK = datetime.now().isocalendar()[1]
CURRENT_YEAR = datetime.now().year


def fetch_and_store_food_selection(session: Session, strategy: FoodProviderStrategy, weeks_to_fetch: int = 3):
    for week in range(CURRENT_WEEK, CURRENT_WEEK + weeks_to_fetch):
        try:
            foods = strategy.fetch_foods_for(CURRENT_YEAR, week)
            _save_food_to_db(session, foods, week)

            raw_data = strategy.get_raw_data(CURRENT_YEAR, week)
            _save_foods_to_json(strategy.get_name().value, raw_data, CURRENT_YEAR, week)

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


def _save_foods_to_json(provider_name: str, data: dict, year: int, week: int):
    filename = SETTINGS.data_dir / f"{provider_name}-week-{year}-{week}.json"
    save_to_json(data, filename)

    JOB_LOGGER.info(f"✅ Week {week} data saved to {filename}.")


if __name__ == "__main__":
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)

    provider_strategies = [
        CityFoodStrategy(),
        InterFoodStrategy(),
    ]

    init_db()
    with Session(engine) as job_session:
        for provider in provider_strategies:
            fetch_and_store_food_selection(job_session, provider)
