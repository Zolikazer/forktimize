from apscheduler.schedulers.background import BackgroundScheduler

from database.db import get_session
from jobs.fetch_food_selection_job import fetch_and_store_cityfood_data
from monitoring.logger import LOGGER

scheduler = BackgroundScheduler()


def run_fetch_job():
    with get_session() as session:
        LOGGER.info("🔄 Running scheduled food data fetch job...")
        fetch_and_store_cityfood_data(session)
