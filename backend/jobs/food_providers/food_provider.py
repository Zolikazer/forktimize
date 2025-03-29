from abc import ABC, abstractmethod
from typing import List

from model.food import Food


class FoodProviderStrategy(ABC):

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> List[Food]:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass
