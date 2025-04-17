from abc import ABC, abstractmethod
from dataclasses import dataclass

from model.food import Food
from food_vendors.food_vendor import FoodVendor

@dataclass
class StrategyResult:
    foods: list[Food]
    images: dict[int, str]
    raw_data: dict

class FoodVendorStrategy(ABC):

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> StrategyResult:
        pass

    @abstractmethod
    def get_raw_data(self, *args, **kwargs) -> dict:
        pass

    @abstractmethod
    def get_food_image_url(self, food_id: int) -> str:
        pass

    @abstractmethod
    def get_name(self) -> FoodVendor:
        pass