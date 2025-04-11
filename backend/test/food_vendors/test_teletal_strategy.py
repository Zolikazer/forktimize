from unittest.mock import Mock, MagicMock

from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal_strategy import TeletalStrategy


def test_teletal_strategy_returns_correct_name():
    menu_page = Mock(spec=TeletalMenuPage)
    food_page = Mock(spec=TeletalFoodPage)

    assert TeletalStrategy(menu_page, food_page).get_name() == FoodVendor.TELETAL


def test_strategy_happy_path():
    menu_page = MagicMock(spec=TeletalMenuPage)
    food_page = MagicMock(spec=TeletalFoodPage)

    menu_page.get_food_category_codes.return_value = ["ZK", "XX"]
    menu_page.get_price.return_value = "1.990 Ft"
    food_page.get_food_data.return_value = {
        "name": "ZabKása",
        "calories": "262.1",
        "protein": "11.3",
        "carb": "26.2",
        "fat": "11.5",
        "year": "2025",
        "week": "15",
        "day": "1",
        "code": "ZK"
    }

    strategy = TeletalStrategy(menu_page, food_page, delay=0)
    foods = strategy.fetch_foods_for(year=2025, week=15)

    assert len(foods) == 10
    menu_page.load.assert_called_once_with(15)
    assert menu_page.get_food_category_codes.call_count == 1
    assert food_page.load.call_count == 10
    assert food_page.get_food_data.call_count == 10


def test_strategy_handles_failures():
    menu_page = MagicMock(spec=TeletalMenuPage)
    food_page = MagicMock(spec=TeletalFoodPage)
    food_page.get_raw_data.return_value = ""

    menu_page.get_food_category_codes.return_value = ["FAIL"]

    def boom_loader(*args, **kwargs):
        raise Exception("💥 food page exploded")

    food_page.load.side_effect = boom_loader

    strategy = TeletalStrategy(menu_page, food_page, delay=0)
    foods = strategy.fetch_foods_for(2025, 15)

    assert foods == []
