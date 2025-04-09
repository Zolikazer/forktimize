from unittest.mock import Mock

from food_vendors.food_vendor import FoodVendor
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_parser import TeletalParser
from food_vendors.strategies.teletal_strategy import TeletalStrategy


def test_teletal_strategy_get_name():
    mock_client = Mock(spec=TeletalClient)
    mock_parser = Mock(spec=TeletalParser)

    assert TeletalStrategy("somehting", mock_client, mock_parser).get_name() == FoodVendor.TELETAL
