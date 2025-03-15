from apscheduler.schedulers.background import BackgroundScheduler

from database.db import get_session
from jobs.fetch_food_selection_job import fetch_and_store_cityfood_data
from model.food import Food
from monitoring.logger import LOGGER

scheduler = BackgroundScheduler()


def is_database_empty():
    session = next(get_session())
    try:
        return session.query(Food).count() == 0
    finally:
        session.close()


def run_fetch_job():
    session = next(get_session())
    LOGGER.info("🔄 Running scheduled food data fetch job...")
    try:
        fetch_and_store_cityfood_data(session)
    finally:
        session.close()
