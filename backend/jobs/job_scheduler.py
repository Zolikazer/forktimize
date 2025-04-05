from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session

from database.db import engine
from jobs.fetch_food_selection_job import fetch_and_store_food_selection
from jobs.food_vendors_strategies.city_food_strategy import CityFoodStrategy
from jobs.food_vendors_strategies.inter_food_strategy import InterFoodStrategy
from monitoring.logging import APP_LOGGER

vendor_strategies = [
    CityFoodStrategy(),
    InterFoodStrategy(),
]

scheduler = BackgroundScheduler()


def run_fetch_job():
    APP_LOGGER.info("🔄 Running scheduled food data fetch job...")
    with Session(engine) as session:
        for vendor in vendor_strategies:
            fetch_and_store_food_selection(session, vendor)
