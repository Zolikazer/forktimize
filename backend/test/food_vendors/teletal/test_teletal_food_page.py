from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup

from exceptions import TeletalUnavailableFoodError
from food_vendors.strategies.teletal.teletal_food_menu_page import TeletalFoodMenuPage
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_single_food_page import TeletalSingleFoodPage
from jobs.serialization import load_file
from test.conftest import YEAR, WEEK, DAY, CODE, TEST_RESOURCES_DIR


def test_parses_food_data_correctly_for_single_food_page():
    food_page_html = load_file(TEST_RESOURCES_DIR / "teletal-food-test.html")

    food_page = TeletalSingleFoodPage(BeautifulSoup(food_page_html, "html.parser"))
    food_data = food_page.get_food_data()

    assert food_data == {"calories": "262.1 kcal",
                         "carb": "26.2 g",
                         "fat": "11.5 g",
                         "name": "ZabKása eperöntettel, édesítőszerekkel",
                         "protein": "11.3 g"}


def test_parses_food_data_correctly_for_menu_page_with_multiple_items():
    food_page_html = load_file(TEST_RESOURCES_DIR / "teletal-food-multiple-test.html")

    food_page = TeletalFoodMenuPage(BeautifulSoup(food_page_html, "html.parser"))
    food_data = food_page.get_menu_data()

    assert food_data == {"calories": "1,340.8 kcal",
                         "carb": "121.10 g",
                         "fat": "44.70 g",
                         "name": "Fokhagymás sült pulykacomb, pikáns párolt lilakáposzta, édesítőszerekkel\n"
                                 "Kemencében sült csirkemell csíkozva, mozzarellás almasaláta\n"
                                 "Sült hekk paprikás lisztben forgatva, zöldborsós jázmin rizs\n"
                                 "Szeletben sült csirkemell, zöldségkrémmártásban, rizi-bizi\n"
                                 "Tiramisu szelet, édesítőszerrel",
                         "protein": "102.00 g"}


@patch("food_vendors.strategies.teletal.teletal_food_page.TeletalFoodMenuPage")
@patch("food_vendors.strategies.teletal.teletal_food_page.TeletalSingleFoodPage")
def test_uses_single_food_parser_when_one_food_present(mock_single_page, mock_menu_page, mock_teletal_client):
    food_page_html = """
    <html><body>
        <h1 class="uk-article-title">Just One Delicious Item</h1>
    </body></html>
    """
    food_name = "Single"
    teletal_client = mock_teletal_client(fetch_food_data=food_page_html)
    mock_single_page.return_value.get_food_data.return_value = {"name": food_name}

    food_page = TeletalFoodPage(teletal_client)
    food_page.load(year=YEAR, week=WEEK, day=DAY, category_code=CODE)
    food_data = food_page.get_food_data()

    assert food_data == {"name": food_name,
                         "code": str(CODE),
                         "year": str(YEAR),
                         "week": str(WEEK),
                         "day": str(DAY), }
    mock_single_page.assert_called_once()
    mock_menu_page.assert_not_called()


@patch("food_vendors.strategies.teletal.teletal_food_page.TeletalFoodMenuPage")
@patch("food_vendors.strategies.teletal.teletal_food_page.TeletalSingleFoodPage")
def test_uses_menu_parser_when_multiple_foods_present(mock_single_page, mock_menu_page, mock_teletal_client):
    food_page_html = """
    <html><body>
        <h1 class="uk-article-title">Menu Title</h1>
        <h1 class="uk-article-title">Food 1</h1>
    </body></html>
    """
    food_name = "Menu"
    teletal_client = mock_teletal_client(fetch_food_data=food_page_html)
    mock_menu_page.return_value.get_menu_data.return_value = {"name": food_name}

    food_page = TeletalFoodPage(teletal_client)
    food_page.load(year=YEAR, week=WEEK, day=DAY, category_code=CODE)
    food_data = food_page.get_food_data()

    assert food_data == {"name": food_name,
                         "code": str(CODE),
                         "year": str(YEAR),
                         "week": str(WEEK),
                         "day": str(DAY), }
    mock_menu_page.assert_called_once()
    mock_single_page.assert_not_called()


def test_raises_when_no_food_name_found_in_html(mock_teletal_client):
    food_page_html = """
    <html><body>
        <h2 class="uk-article-title">Menu Title</h2>
    </body></html>
    """
    teletal_client = mock_teletal_client(fetch_food_data=food_page_html)

    food_page = TeletalFoodPage(teletal_client)
    food_page.load(year=YEAR, week=WEEK, day=DAY, category_code=CODE)

    with pytest.raises(AssertionError, match="No food names were found – expected 1 or multiple <h1> tags"):
        food_page.get_food_data()

def test_load_calls_fetch_food_data_with_correct_params(mock_teletal_client):
    teletal_client = mock_teletal_client()
    food_page = TeletalFoodPage(teletal_client)

    food_page.load(year=YEAR, week=WEEK, day=DAY, category_code=CODE)

    teletal_client.fetch_food_data.assert_called_once_with(
        year=YEAR, week=WEEK, day=DAY, code=CODE
    )


def test_returns_original_html_after_loading(mock_teletal_client):
    food_available_html = """
                <main>
                    <h1 class="uk-article-title">Brokkolis rizs</h1>
                </main>
                """
    teletal_client = mock_teletal_client(fetch_food_data=food_available_html)

    page = TeletalFoodPage(teletal_client)
    page.load(year=YEAR, week=WEEK, day=DAY, category_code=CODE)

    raw_data = page.get_raw_data()
    assert "Brokkolis rizs" in raw_data
    assert "<main>" in raw_data


def test_raises_if_get_food_data_called_without_loading_page(mock_teletal_client):
    food_page = TeletalFoodPage(mock_teletal_client())

    with pytest.raises(AssertionError, match="You must call load\\(\\) first"):
        food_page.get_food_data()


def test_raises_unavailable_error_when_info_missing_on_page(mock_teletal_client):
    food_not_available_html = """
                <main>
                    <h2>Jelenleg sajnos nem érhető el információ!</h2>
                </main>
                """
    teletal_client = mock_teletal_client(fetch_food_data=food_not_available_html)

    page = TeletalFoodPage(teletal_client)
    page.load(year=2025, week=16, day=1, category_code="GHOST")

    with pytest.raises(TeletalUnavailableFoodError):
        page.get_food_data()
