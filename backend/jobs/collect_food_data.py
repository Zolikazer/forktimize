import time
from datetime import datetime

from sqlmodel import Session

from database.db import init_db, engine
from jobs.food_vendors_strategies.food_vendor_strategy import FoodVendorStrategy
from jobs.food_vendors_strategies.vendor_strategies import VENDOR_STRATEGIES
from model.food_vendors import FoodVendor
from jobs.serialization import save_to_json
from model.food import Food
from model.job_run import JobRun, JobStatus
from monitoring.logging import JOB_LOGGER, APP_LOGGER
from settings import SETTINGS

def run_collect_food_data_job():
    APP_LOGGER.info("🔄 Running scheduled food data fetch job...")
    with Session(engine) as session:
        collect_food_data(session, VENDOR_STRATEGIES)

def collect_food_data(session: Session, strategies: list[FoodVendorStrategy], weeks_to_fetch=SETTINGS.WEEKS_TO_FETCH,
                      delay=SETTINGS.FETCHING_DELAY):
    current_year = datetime.now().year
    current_week = datetime.now().isocalendar()[1]

    for strategy in strategies:
        for week in range(current_week, current_week + weeks_to_fetch):
            try:
                _sync_food_data(session, current_year, current_week, strategy)
                _track_successful_job_run(current_year, session, strategy, week)
            except Exception as e:
                _track_failed_job_jon(current_year, e, session, strategy, week)

            time.sleep(delay)


def _sync_food_data(session: Session, year: int, week: int, strategy: FoodVendorStrategy):
    foods = strategy.fetch_foods_for(year, week)
    _save_food_to_db(session, foods, week)

    raw_data = strategy.get_raw_data(year, week)
    _save_foods_to_json(strategy.get_name().value, raw_data, year, week)


def _save_food_to_db(session: Session, foods: list[Food], week: int):
    for food in foods:
        session.merge(food)

    session.commit()

    JOB_LOGGER.info(f"✅ Week {week} food selection stored in the database.")


def _save_foods_to_json(vendor_name: str, data: dict, year: int, week: int):
    filename = SETTINGS.data_dir / f"{vendor_name}-week-{year}-{week}.json"
    save_to_json(data, filename)

    JOB_LOGGER.info(f"✅ Week {week} data saved to {filename}.")


def _track_failed_job_jon(current_year, e, session, strategy, week):
    job_id = _track_job_run(session, week, current_year, JobStatus.FAILURE, strategy.get_name())
    JOB_LOGGER.error(f"❌ Job ID={job_id}: Unexpected error: {e}")


def _track_successful_job_run(current_year, session, strategy, week):
    job_id = _track_job_run(session, week, current_year, JobStatus.SUCCESS, strategy.get_name())
    JOB_LOGGER.info(
        f"✅ Job ID={job_id}: Successfully fetched & stored data for {strategy.get_name()} Week {week}.")


def _track_job_run(session: Session, week: int, year: int, status: JobStatus, vendor: FoodVendor) -> int:
    job_run = JobRun(week=week, year=year, status=status, timestamp=datetime.now(), food_vendor=vendor)
    session.add(job_run)
    session.commit()
    session.refresh(job_run)

    JOB_LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Week={week}, Year={year}, Status={status}")
    return job_run.id


if __name__ == "__main__":
    SETTINGS.data_dir.mkdir(parents=True, exist_ok=True)

    init_db()
    with Session(engine) as job_session:
        collect_food_data(job_session, VENDOR_STRATEGIES)
