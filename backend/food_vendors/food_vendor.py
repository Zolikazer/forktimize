from __future__ import annotations

from datetime import date

from sqlmodel import Session

from database.data_access import get_available_dates_for_vendor
from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_collection_strategy import FoodCollectionStrategy
from food_vendors.strategies.inter_city_food.city_food_strategy import CityFoodStrategy
from food_vendors.strategies.inter_city_food.inter_food_strategy import InterFoodStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy
from settings import SETTINGS


class FoodVendor:
    def __init__(self, vendor_type: FoodVendorType, strategy: FoodCollectionStrategy, name: str, menu_url: str):
        self._food_vendor_type: FoodVendorType = vendor_type
        self._strategy: FoodCollectionStrategy = strategy
        self._menu_url: str = menu_url
        self._name: str = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> FoodVendorType:
        return self._food_vendor_type

    @property
    def strategy(self) -> FoodCollectionStrategy:
        return self._strategy

    @property
    def menu_url(self) -> str:
        return self._menu_url

    def get_available_dates(self, session: Session) -> list[date]:
        return get_available_dates_for_vendor(session, date.today(), self._food_vendor_type)


def _create_vendor_registry() -> dict[FoodVendorType, FoodVendor]:
    teletal_client = TeletalClient()
    return {
        FoodVendorType.CITY_FOOD:
            FoodVendor(
                FoodVendorType.CITY_FOOD,
                CityFoodStrategy(),
                "Cityfood",
                SETTINGS.CITY_FOOD_MENU_URL),
        FoodVendorType.INTER_FOOD:
            FoodVendor(
                FoodVendorType.INTER_FOOD,
                InterFoodStrategy(),
                "Interfood",
                SETTINGS.INTER_FOOD_ORDERING_URL,
            ),
        FoodVendorType.TELETAL:
            FoodVendor(
                FoodVendorType.TELETAL,
                TeletalStrategy(TeletalMenuPage(teletal_client), TeletalFoodPage(teletal_client)),
                "Teletál",
                SETTINGS.TELETAL_MENU_URL
            )
    }


VENDOR_REGISTRY = _create_vendor_registry()
