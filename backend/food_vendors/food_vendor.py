from __future__ import annotations

from datetime import date

from sqlmodel import Session

from database.data_access import get_available_dates_for_vendor
from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy
from food_vendors.strategies.inter_city_food.city_food_strategy import CityFoodStrategy
from food_vendors.strategies.inter_city_food.inter_food_strategy import InterFoodStrategy
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy
from settings import SETTINGS


class FoodVendor:
    def __init__(self, vendor_type: FoodVendorType, strategy: FoodVendorStrategy, name: str, menu_url: str):
        self._food_vendor_type: FoodVendorType = vendor_type
        self._strategy: FoodVendorStrategy = strategy
        self._menu_url = menu_url
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> FoodVendorType:
        return self._food_vendor_type

    @property
    def strategy(self) -> FoodVendorStrategy:
        return self._strategy

    @property
    def menu_url(self) -> str:
        return self._menu_url

    def get_available_dates(self, session: Session) -> list[date]:
        return get_available_dates_for_vendor(session, date.today(), self._food_vendor_type)


def _get_vendor_registry() -> dict[FoodVendorType, FoodVendor]:
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
                "Teletáletal",
                SETTINGS.TELETAL_MENU_URL
            )
    }


VENDOR_REGISTRY = _get_vendor_registry()
