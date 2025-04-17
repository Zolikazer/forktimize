from __future__ import annotations

from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.inter_city_food.city_food_strategy import CityFoodStrategy
from food_vendors.strategies.inter_city_food.inter_food_strategy import InterFoodStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy


class FoodVendor:
    def __init__(self, vendor_type: FoodVendorType, strategy: FoodVendorStrategy):
        self._food_vendor_type: FoodVendorType = vendor_type
        self._strategy: FoodVendorStrategy = strategy

    @property
    def type(self) -> FoodVendorType:
        return self._food_vendor_type

    @property
    def strategy(self) -> FoodVendorStrategy:
        return self._strategy


def _get_vendor_registry() -> dict[FoodVendorType, FoodVendor]:
    teletal_client = TeletalClient()
    return {
        FoodVendorType.CITY_FOOD: FoodVendor(FoodVendorType.CITY_FOOD, CityFoodStrategy()),
        FoodVendorType.INTER_FOOD: FoodVendor(FoodVendorType.INTER_FOOD, InterFoodStrategy()),
        FoodVendorType.TELETAL: FoodVendor(
            FoodVendorType.TELETAL,
            TeletalStrategy(TeletalMenuPage(teletal_client), TeletalFoodPage(teletal_client))
        )
    }


VENDOR_REGISTRY = _get_vendor_registry()
