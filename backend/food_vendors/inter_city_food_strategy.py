from abc import ABC, abstractmethod
from datetime import datetime

import requests

from food_vendors.food_vendor_strategy import FoodVendorStrategy
from model.food import Food
from model.food_vendors import FoodVendor
from monitoring.logging import JOB_LOGGER


class InterCityFoodStrategy(FoodVendorStrategy, ABC):

    @abstractmethod
    def __init__(self, api_endpoint: str, food_vendor: FoodVendor):
        self._api_endpoint: str = api_endpoint
        self._food_vendor: FoodVendor = food_vendor
        self._raw_data: dict = {}

    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        data = self.get_raw_data(year, week)
        foods = self._deserialize_food_items(data)

        JOB_LOGGER.info(f"✅ Fetched {len(foods)} foods from {self._food_vendor.value} for week {week}, year {year}.")

        return foods

    def get_raw_data(self, year: int, week: int) -> dict:
        if self._raw_data.get(f"{year}{week}") is None:
            response = requests.post(self._api_endpoint, json=self._get_request_body(year, week), timeout=10)
            response.raise_for_status()
            self._raw_data[f"{year}{week}"] = response.json()

        return self._raw_data[f"{year}{week}"]

    def get_name(self) -> FoodVendor:
        return self._food_vendor

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
                food_vendor=self.get_name()
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
