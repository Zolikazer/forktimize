from unittest.mock import MagicMock

import pytest

from food_vendors.strategies.teletal.teletal_client import TeletalClient

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
