from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup

from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_menu_page import TeletalFoodMenuPage
from food_vendors.strategies.teletal.teletal_food_page import TeletalFoodPage
from food_vendors.strategies.teletal.teletal_single_food_page import TeletalSingleFoodPage
from test.common import TEST_RESOURCES_DIR


def load_test_html(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def test_food_page_returns_correct_food_data():
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

    with patch("food_vendors.strategies.teletal.teletal_food_page.TeletalSingleFoodPage") as mock_single_page, \
            patch("food_vendors.strategies.teletal.teletal_food_page.TeletalFoodMenuPage") as mock_menu_page:
        mock_single_page.return_value.get_food_data.return_value = {"name": "Single"}
        food_page = TeletalFoodPage(mock_client)

        result = food_page.get_food_data(year=2025, week=15, category_code="ZK", day=1)

        assert result["name"] == "Single"
        assert result["code"] == "ZK"
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

    with patch("food_vendors.strategies.teletal.teletal_food_page.TeletalSingleFoodPage") as mock_single_page, \
            patch("food_vendors.strategies.teletal.teletal_food_page.TeletalFoodMenuPage") as mock_menu_page:
        mock_menu_page.return_value.get_menu_data.return_value = {"name": "Menu"}
        food_page = TeletalFoodPage(mock_client)

        result = food_page.get_food_data(year=2025, week=15, category_code="ZK", day=1)

        assert result["name"] == "Menu"
        assert result["code"] == "ZK"
        mock_menu_page.assert_called_once()
        mock_single_page.assert_not_called()

