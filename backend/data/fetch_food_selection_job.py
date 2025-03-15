from datetime import datetime
from pathlib import Path

import requests
from sqlmodel import Session

from data.data_loader import serialize_food_items, save_to_json
from database.db import init_db, get_session
from model.job_run import JobRun, JobStatus
from monitoring.logger import LOGGER
from settings import SETTINGS

DATA_ENDPOINT = f"{SETTINGS.CITY_FOOD_API_URL}/{SETTINGS.CITY_FOOD_API_FOOD_PATH}"
RESOURCES_DIR = Path(__file__).parent.parent.resolve() / SETTINGS.DATA_DIR
CURRENT_WEEK = datetime.now().isocalendar()[1]
CURRENT_YEAR = datetime.now().year


def fetch_and_store_cityfood_data(session: Session, weeks_to_fetch: int = 3):
    for week in range(CURRENT_WEEK, CURRENT_WEEK + weeks_to_fetch):
        try:
            data = _fetch_food_selection_for(week)
            _save_food_to_json(data, week)
            _save_food_to_db(session, data, week)

            job_id = _track_job_run(session, week, CURRENT_YEAR, JobStatus.SUCCESS)
            LOGGER.info(f"✅ Job ID={job_id}: Successfully fetched & stored data for Week {week}.")
        except Exception as e:
            job_id = _track_job_run(session, week, CURRENT_YEAR, JobStatus.FAILURE)
            LOGGER.error(f"❌ Job ID={job_id}: Unexpected error: {e}")


def _save_food_to_json(data, week):
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)
    filename = RESOURCES_DIR / f"city-response-week-{week}.json"
    save_to_json(data, filename)

    LOGGER.info(f"✅ Week {week} data saved to {filename}.")


def _save_food_to_db(session: Session, data: dict, week: int):
    foods = serialize_food_items(data)

    for food in foods:
        session.merge(food)

    session.commit()

    LOGGER.info(f"✅ Week {week} food selection stored in the database.")


def _fetch_food_selection_for(week: int) -> dict:
    response = requests.post(DATA_ENDPOINT, json=_get_request_body(CURRENT_YEAR, week), timeout=10)
    response.raise_for_status()
    data = response.json()

    return data


def _track_job_run(session: Session, week: int, year: int, status: JobStatus) -> int:
    job_run = JobRun(week=week, year=year, status=status, timestamp=datetime.now())
    session.add(job_run)
    session.commit()
    session.refresh(job_run)

    LOGGER.info(f"📌 Job Run Logged: ID={job_run.id}, Week={week}, Year={year}, Status={status}")
    return job_run.id


def _get_request_body(year: int, week: int) -> dict:
    return {"year": str(year), "week": str(week), "calorie": {"min": 0, "max": 9000}, "carb": {"min": 0, "max": 9000},
            "protein": {"min": 0, "max": 9000}, "fat": {"min": 0, "max": 9000}, "price": {"min": 0, "max": 9000},
            "favorites": False, "last_minute": False, "seek_labels": [], "ignore_labels": [], "seek_ingredients": [],
            "ignore_ingredients": []}


if __name__ == "__main__":
    init_db()
    with next(get_session()) as db_session:
        fetch_and_store_cityfood_data(db_session)
