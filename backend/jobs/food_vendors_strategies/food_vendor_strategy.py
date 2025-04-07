from abc import ABC, abstractmethod

from model.food import Food
from model.food_vendors import FoodVendor


class FoodVendorStrategy(ABC):

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> list[Food]:
        pass

    @abstractmethod
    def get_raw_data(self, year: int, week: int) -> dict:
        pass

    @abstractmethod
    def get_name(self) -> FoodVendor:
        pass

    @abstractmethod
    def get_food_image_url(self, food_id: int) -> str:
        pass