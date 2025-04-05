from abc import ABC, abstractmethod
from typing import List

from model.food_vendors import FoodVendor
from model.food import Food


class FoodVendorStrategy(ABC):

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> List[Food]:
        pass

    @abstractmethod
    def get_raw_data(self, year: int, week: int) -> dict:
        pass

    @abstractmethod
    def get_name(self) -> FoodVendor:
        pass
