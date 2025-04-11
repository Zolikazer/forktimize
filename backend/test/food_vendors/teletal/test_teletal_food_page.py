from unittest.mock import MagicMock, patch, Mock

import pytest
from bs4 import BeautifulSoup

from error_handling.exceptions import TeletalUnavailableFoodError
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_menu_page import TeletalFoodMenuPage
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_single_food_page import TeletalSingleFoodPage
from test.common import TEST_RESOURCES_DIR


def load_test_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_single_food_page_returns_correct_food_data():
    test_file = TEST_RESOURCES_DIR / "teletal-food-test.html"
    food_page_html = load_test_html(test_file)

    food_page = TeletalSingleFoodPage(BeautifulSoup(food_page_html, "html.parser"))
    food_data = food_page.get_food_data()

    assert food_data == {"calories": "262.1 kcal",
                         "carb": "26.2 g",
                         "fat": "11.5 g",
                         "name": "ZabKása eperöntettel, édesítőszerekkel",
                         "protein": "11.3 g"}


def test_menu_page_returns_correct_food_data():
    test_file = TEST_RESOURCES_DIR / "teletal-food-multiple-test.html"
    food_page_html = load_test_html(test_file)

    mock_client = MagicMock(spec=TeletalClient)
    mock_client.fetch_food_data.return_value = food_page_html

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


def test_food_page_get_food_data_delegates_to_single_food_page():
    fake_html = """
    <html><body>
        <h1 class="uk-article-title">Just One Delicious Item</h1>
    </body></html>
    """

    mock_client = MagicMock(spec=TeletalClient)
    mock_client.fetch_food_data.return_value = fake_html
    year = 2025
    week = 15
    day = 1
    code = "ZK"

    with patch("food_vendors.strategies.teletal.teletal_food_page.TeletalSingleFoodPage") as mock_single_page, \
            patch("food_vendors.strategies.teletal.teletal_food_page.TeletalFoodMenuPage") as mock_menu_page:
        mock_single_page.return_value.get_food_data.return_value = {"name": "Single"}
        food_page = TeletalFoodPage(mock_client)

        food_page.load(year=year, week=week, day=day, category_code=code)
        food_data = food_page.get_food_data()

        assert food_data["name"] == "Single"
        assert food_data["code"] == str(code)
        assert food_data["year"] == str(year)
        assert food_data["week"] == str(week)
        assert food_data["day"] == str(day)

        mock_single_page.assert_called_once()
        mock_menu_page.assert_not_called()


def test_food_page_get_food_data_delegates_to_food_menu_page():
    fake_html = """
    <html><body>
        <h1 class="uk-article-title">Menu Title</h1>
        <h1 class="uk-article-title">Food 1</h1>
        <h1 class="uk-article-title">Food 2</h1>
    </body></html>
    """

    mock_client = MagicMock(spec=TeletalClient)
    mock_client.fetch_food_data.return_value = fake_html
    year = 2025
    week = 15
    day = 1
    code = "ZK"
    with patch("food_vendors.strategies.teletal.teletal_food_page.TeletalSingleFoodPage") as mock_single_page, \
            patch("food_vendors.strategies.teletal.teletal_food_page.TeletalFoodMenuPage") as mock_menu_page:
        mock_menu_page.return_value.get_menu_data.return_value = {"name": "Menu"}
        food_page = TeletalFoodPage(mock_client)

        food_page.load(year=year, week=week, category_code=code, day=day)
        food_data = food_page.get_food_data()

        assert food_data["name"] == "Menu"
        assert food_data["code"] == str(code)
        assert food_data["year"] == str(year)
        assert food_data["week"] == str(week)
        assert food_data["day"] == str(day)
        mock_menu_page.assert_called_once()
        mock_single_page.assert_not_called()


def test_food_page_get_food_data_throws_exception_if_no_name_found():
    fake_html = """
    <html><body>
        <h2 class="uk-article-title">Menu Title</h2>
    </body></html>
    """

    mock_client = MagicMock(spec=TeletalClient)
    mock_client.fetch_food_data.return_value = fake_html

    food_page = TeletalFoodPage(mock_client)
    food_page.load(year=2025, week=15, day=3, category_code="R1")

    with pytest.raises(AssertionError, match="No food names were found – expected 1 or multiple <h1> tags"):
        food_page.get_food_data()


def test_food_page_raises_if_get_called_before_load():
    client = Mock(spec=TeletalClient)
    page = TeletalFoodPage(client)

    with pytest.raises(AssertionError, match="You must call load\\(\\) first"):
        page.get_food_data()


def test_food_page_returns_original_html():
    food_available_html = """
                <main>
                    <h1 class="uk-article-title">Brokkolis rizs</h1>
                </main>
                """
    client = MagicMock()
    client.fetch_food_data.return_value = food_available_html

    page = TeletalFoodPage(client)
    page.load(year=2025, week=16, day=1, category_code="BROK")

    raw_data = page.get_raw_data()
    assert "Brokkolis rizs" in raw_data
    assert "<main>" in raw_data


def test_food_page_throws_exception_if_no_data_available():
    food_not_available_html = """
                <main>
                    <h2>Jelenleg sajnos nem érhető el információ!</h2>
                </main>
                """
    client = MagicMock()
    client.fetch_food_data.return_value = food_not_available_html

    page = TeletalFoodPage(client)
    page.load(year=2025, week=16, day=1, category_code="GHOST")

    with pytest.raises(TeletalUnavailableFoodError):
        page.get_food_data()
