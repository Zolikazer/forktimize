from unittest.mock import MagicMock, patch

import pytest

from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy
from test.conftest import YEAR, WEEK


def boom_loader(*args, **kwargs):
    raise Exception("💥 food page exploded")


@pytest.fixture
def mock_menu_page():
    def _make_menu_page(get_food_category_codes: list[str] = None, get_price: str = "") -> MagicMock:
        menu_page = MagicMock(spec=TeletalMenuPage)
        menu_page.get_food_category_codes.return_value = get_food_category_codes
        menu_page.get_price.return_value = get_price

        return menu_page

    return _make_menu_page


@pytest.fixture
def mock_food_page():
    def _make_food_page(get_food_data: dict[str, str] = None, get_raw_data: str = "") -> MagicMock:
        food_page = MagicMock(spec=TeletalFoodPage)
        food_page.get_food_data.return_value = get_food_data
        food_page.get_raw_data.return_value = get_raw_data
        return food_page

    return _make_food_page

def test_get_vendor__returns_teletal_enum(mock_menu_page, mock_food_page):
    assert TeletalStrategy(mock_menu_page(), mock_food_page()).get_vendor() == FoodVendor.TELETAL


def test_strategy_result_contains_correct_vendor(mock_menu_page, mock_food_page):
    menu_page = mock_menu_page(get_food_category_codes=["ZK", "XX"])
    food_page = mock_food_page(get_food_data={})

    result = TeletalStrategy(menu_page, food_page, delay=0).fetch_foods_for(YEAR, WEEK)
    assert result.vendor == FoodVendor.TELETAL


def test_fetch_foods_for__calls_menu_and_food_page_properly(mock_menu_page, mock_food_page):
    menu_page = mock_menu_page(get_food_category_codes=["ZK", "XX"])
    food_page = mock_food_page(get_food_data={})

    strategy = TeletalStrategy(menu_page, food_page, delay=0)
    strategy.fetch_foods_for(year=YEAR, week=WEEK)

    menu_page.load.assert_called_once_with(WEEK)
    assert menu_page.get_food_category_codes.call_count == 1
    assert food_page.load.call_count == 10
    assert food_page.get_food_data.call_count == 10
    assert menu_page.get_price.call_count == 10


def test_fetch_foods_for__parses_and_returns_all_foods_correctly(mock_menu_page, mock_food_page):
    menu_page = mock_menu_page(get_food_category_codes=["ZK", "XX"], get_price="1.990 Ft")
    food_page = mock_food_page(get_food_data={
        "name": "ZabKása",
        "calories": "262.1",
        "protein": "11.3",
        "carb": "26.2",
        "fat": "11.5",
        "year": "2025",
        "week": "15",
        "day": "1",
        "code": "ZK"
    })

    strategy = TeletalStrategy(menu_page, food_page, delay=0)
    result = strategy.fetch_foods_for(year=YEAR, week=WEEK)

    assert len(result.foods) == 10
    assert all(f.name == "ZabKása" for f in result.foods)
    assert all(f.price == 1990 for f in result.foods)


@patch("food_vendors.strategies.teletal.teletal_strategy.save_file")
def test_fetch_foods_for__handles_exceptions(mock_menu_page, mock_food_page):
    menu_page = mock_menu_page(get_food_category_codes=["R1"])
    food_page = mock_food_page()
    food_page.load.side_effect = boom_loader

    strategy = TeletalStrategy(menu_page, food_page, delay=0)
    result = strategy.fetch_foods_for(YEAR, WEEK)

    assert result.foods == []
    assert result.images == {}
    assert result.raw_data == []


@patch("food_vendors.strategies.teletal.teletal_strategy.save_file")
def test_fetch_foods_for__handles_exceptions_saves_debug_file(mock_save_file, mock_menu_page, mock_food_page):
    food_page = mock_food_page()
    menu_page = mock_menu_page(get_food_category_codes=["R1"])
    food_page.load.side_effect = boom_loader

    strategy = TeletalStrategy(menu_page, food_page, delay=0)
    strategy.fetch_foods_for(2025, 15)

    assert mock_save_file.call_count == 5
    assert "debug_food_page_R1_5.html" in str(mock_save_file.call_args[0][1])


def test_get_food_image_url_after_fetch_success_with_image(mock_food_page, mock_menu_page):
    teletal_url = f"https://www.test.hu"
    image_url = "banana.png"
    menu_page = mock_menu_page(get_food_category_codes=["ZK"], get_price="1.990 Ft")
    food_page = mock_food_page(get_food_data={
        "name": "ZabKása",
        "calories": "262.1",
        "protein": "11.3",
        "carb": "26.2",
        "fat": "11.5",
        "year": "2025",
        "week": "15",
        "day": "1",
        "code": "ZK",
        "image": image_url
    })

    strategy = TeletalStrategy(menu_page, food_page, teletal_url=teletal_url, delay=0)
    result = strategy.fetch_foods_for(year=YEAR, week=WEEK)

    assert result.images[758637169892] == f"{teletal_url}/{image_url}"
