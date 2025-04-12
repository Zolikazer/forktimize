import itertools
from datetime import date as datetime_date
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from model.food import Food

YEAR = 2025
WEEK = 16
DAY = 1
CODE = "ZK"


@pytest.fixture
def mock_teletal_client():
    def _make(
            get_main_menu: str = "",
            get_dynamic_category: str = "",
            fetch_food_data: str = "",
    ) -> MagicMock:
        client = MagicMock(spec=TeletalClient)
        client.get_main_menu.return_value = get_main_menu
        client.get_dynamic_category.return_value = get_dynamic_category
        client.fetch_food_data.return_value = fetch_food_data
        return client

    return _make


TEST_RESOURCES_DIR = Path(__file__).parent.resolve() / "resources"


def make_food(
        food_id: int = None,
        name: str = None,
        food_vendor: FoodVendor = FoodVendor.CITY_FOOD,
        date: datetime_date = datetime_date(2025, 2, 24),
        calories: int = 500,
        protein: int = 50,
        carb: int = 50,
        fat: int = 11,
        price: int = 1000
) -> Food:
    if food_id is None:
        food_id = next(_food_id_counter)
    if name is None:
        name = f"Test Chicken {food_id}"

    return Food(
        food_id=food_id,
        name=name,
        food_vendor=food_vendor,
        date=date,
        calories=calories,
        protein=protein,
        carb=carb,
        fat=fat,
        price=price
    )


_food_id_counter = itertools.count(1)
