from apscheduler.schedulers.background import BackgroundScheduler
from sqlmodel import Session

from database.db import engine
from jobs.fetch_food_selection_job import fetch_and_store_food_selection
from jobs.food_providers.city_food_strategy import CityFoodStrategy
from jobs.food_providers.inter_food_strategy import InterFoodStrategy
from monitoring.logging import APP_LOGGER

providers = [
    CityFoodStrategy(),
    InterFoodStrategy(),
]

scheduler = BackgroundScheduler()


def run_fetch_job():
    APP_LOGGER.info("🔄 Running scheduled food data fetch job...")
    with Session(engine) as session:
        for provider in providers:
            fetch_and_store_food_selection(session, provider)
