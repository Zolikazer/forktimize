from datetime import datetime
from typing import List

import requests

from jobs.food_providers.food_provider_strategy import FoodProviderStrategy
from jobs.food_providers.food_providers import FoodProvider
from model.food import Food
from monitoring.logging import JOB_LOGGER


class InterCityFoodProvider(FoodProviderStrategy):

    def __init__(self, api_endpoint: str, food_provider: FoodProvider):
        self._api_endpoint = api_endpoint
        self._food_provider = food_provider
        self._raw_data = {}

    def fetch_foods_for(self, year: int, week: int) -> List[Food]:
        data = self.get_raw_data(year, week)
        self._raw_data[f"{year}{week}"] = data
        foods = self._deserialize_food_items(data)

        JOB_LOGGER.info(f"✅ Fetched {len(foods)} foods from CityFood for week {week}, year {year}.")

        return foods

    def get_raw_data(self, year: int, week: int) -> dict:
        if self._raw_data.get(f"{year}{week}") is None:
            response = requests.post(self._api_endpoint, json=self._get_request_body(year, week), timeout=10)
            response.raise_for_status()
            self._raw_data[f"{year}{week}"] = response.json()

        return self._raw_data[f"{year}{week}"]

    def get_name(self) -> FoodProvider:
        return self._food_provider

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
                food_provider=self.get_name()
            )
            for food_type in data['data'].values()
            for category in food_type['categories']
            for item in category['items']
        ]

    @staticmethod
    def _get_request_body(year: int, week: int) -> dict:
        return {"year": str(year), "week": str(week), "calorie": {"min": 0, "max": 9000},
                "carb": {"min": 0, "max": 9000},
                "protein": {"min": 0, "max": 9000}, "fat": {"min": 0, "max": 9000}, "price": {"min": 0, "max": 9000},
                "favorites": False, "last_minute": False, "seek_labels": [], "ignore_labels": [],
                "seek_ingredients": [],
                "ignore_ingredients": []}
