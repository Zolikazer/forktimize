from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass

from model.food import Food
from food_vendors.food_vendor_type import FoodVendorType


@dataclass
class StrategyResult:
    foods: list[Food]
    images: dict[int, str]
    raw_data: dict | list
    vendor: FoodVendorType


class FoodVendorStrategy(ABC):

    @abstractmethod
    def fetch_foods_for(self, year: int, week: int) -> StrategyResult:
        pass

    @abstractmethod
    def get_vendor(self) -> FoodVendorType:
        pass
