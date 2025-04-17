from abc import ABC, abstractmethod
from datetime import datetime

import requests

from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy, StrategyResult
from model.food import Food
from food_vendors.food_vendor import FoodVendor
from monitoring.logging import JOB_LOGGER


class InterCityFoodStrategy(FoodVendorStrategy, ABC):

    @abstractmethod
    def __init__(self, api_endpoint: str, food_image_url: str, food_vendor: FoodVendor):
        self._api_endpoint: str = api_endpoint
        self._food_image_url: str = food_image_url
        self._food_vendor: FoodVendor = food_vendor

    def fetch_foods_for(self, year: int, week: int) -> StrategyResult:
        response = requests.post(self._api_endpoint, json=self._get_request_body(year, week), timeout=10)
        response.raise_for_status()
        raw_data = response.json()

        foods = self._deserialize_food_items(raw_data)
        JOB_LOGGER.info(f"✅ Fetched {len(foods)} foods from {self._food_vendor.value} for week {week}, year {year}.")

        return StrategyResult(foods=foods,
                              raw_data=raw_data,
                              images={f.food_id: self._food_image_url.format(food_id=f.food_id) for f
                                      in foods})

    def get_raw_data(self) -> dict:
        return {}

    def get_name(self) -> FoodVendor:
        return self._food_vendor

    def _deserialize_food_items(self, raw_data: dict) -> list[Food]:
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
            for food_type in raw_data['data'].values()
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
