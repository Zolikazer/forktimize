from abc import ABC, abstractmethod
from typing import List

from jobs.food_providers.food_providers import FoodProvider
from model.food import Food


class FoodProviderStrategy(ABC):

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> List[Food]:
        pass

    @abstractmethod
    def get_raw_data(self, year: int, week: int) -> dict:
        pass

    @abstractmethod
    def get_name(self) -> FoodProvider:
        pass
