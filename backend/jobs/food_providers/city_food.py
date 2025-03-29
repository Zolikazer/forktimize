from datetime import datetime
from pathlib import Path
from typing import List

import requests

from jobs.food_providers.food_provider import FoodProviderStrategy
from jobs.serialization import save_to_json
from model.food import Food, FoodProvider
from monitoring.logging import JOB_LOGGER
from settings import SETTINGS


class CityFoodProvider(FoodProviderStrategy):
    def fetch_foods_for(self, year: int, week: int) -> List[Food]:
        raw_data = self._fetch_food_selection_for(year, week)
        self._save_foods_to_json(raw_data, year, week)
        foods = self._deserialize_food_items(raw_data)

        JOB_LOGGER.info(f"✅ Fetched {len(foods)} foods from CityFood for week {week}, year {year}.")

        return foods

    def get_name(self) -> FoodProvider:
        return FoodProvider.CITY_FOOD

    def _fetch_food_selection_for(self, year: int, week: int) -> dict:
        response = requests.post(f"{SETTINGS.CITY_FOOD_API_URL}/{SETTINGS.CITY_FOOD_API_FOOD_PATH}",
                                 json=self._get_request_body(year, week), timeout=10)
        response.raise_for_status()
        data = response.json()

        return data

    def _get_request_body(self, year: int, week: int) -> dict:
        return {"year": str(year), "week": str(week), "calorie": {"min": 0, "max": 9000},
                "carb": {"min": 0, "max": 9000},
                "protein": {"min": 0, "max": 9000}, "fat": {"min": 0, "max": 9000}, "price": {"min": 0, "max": 9000},
                "favorites": False, "last_minute": False, "seek_labels": [], "ignore_labels": [],
                "seek_ingredients": [],
                "ignore_ingredients": []}

    def _save_foods_to_json(self, data: dict, year: int, week: int):
        filename = SETTINGS.DATA_DIR / f"city-response-week-{year}-{week}.json"
        save_to_json(data, SETTINGS.DATA_DIR / f"city-response-week-{year}-{week}.json")

        JOB_LOGGER.info(f"✅ Week {week} data saved to {filename}.")

    def _deserialize_food_items(self, data: dict) -> list[Food]:
        return [
            Food(
                food_id=item['id'],
                name=item["food"]['name'],
                calories=item['energy_portion_food_one'],
                protein=int(item['protein_portion_food_one']),
                carb=int(item['carb_portion_food_one']),
                fat=int(item['fat_portion_food_one']),
                price=item['price'],
                date=datetime.strptime(item['date'], "%Y-%m-%d").date(),
                food_provider=FoodProvider.CITY_FOOD
            )
            for food_type in data['data'].values()
            for category in food_type['categories']
            for item in category['items']
        ]
