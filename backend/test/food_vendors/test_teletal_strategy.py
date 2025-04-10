from unittest.mock import Mock

from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from food_vendors.strategies.teletal_strategy import TeletalStrategy


def test_teletal_strategy_get_name():
    mock_client = Mock(spec=TeletalClient)
    menu_page = Mock(spec=TeletalMenuPage)

    assert TeletalStrategy(mock_client, menu_page).get_name() == FoodVendor.TELETAL
