from datetime import date

import pytest
from unittest.mock import Mock, patch

from freezegun import freeze_time
from sqlmodel import Session

from food_vendors.food_vendor import FoodVendor
from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_vendor_strategy import FoodCollectionStrategy
from food_vendors.strategies.teletal.teletal_strategy import TeletalStrategy


def test_food_vendor_properties():
    mock_strategy = Mock(spec=FoodCollectionStrategy)
    vendor_name = "something"
    vendor_url = "dsfdsfs"
    vendor = FoodVendor(FoodVendorType.TELETAL, mock_strategy, vendor_name, vendor_url)

    assert vendor.type == FoodVendorType.TELETAL
    assert vendor.strategy is mock_strategy
    assert vendor.name == vendor_name
    assert vendor.menu_url == vendor_url


def test_food_vendor_type_is_read_only():
    mock_strategy = Mock(spec=FoodCollectionStrategy)
    vendor = FoodVendor(FoodVendorType.CITY_FOOD, mock_strategy, "something", "dsfds")

    with pytest.raises(AttributeError):
        vendor.type = FoodVendorType.TELETAL


def test_food_vendor_strategy_is_read_only():
    mock_strategy = Mock(spec=FoodCollectionStrategy)
    vendor = FoodVendor(FoodVendorType.INTER_FOOD, mock_strategy, "something", "dfd")

    with pytest.raises(AttributeError):
        vendor.strategy = Mock(spec=FoodCollectionStrategy)


def test_food_vendor_menu_url_is_read_only():
    mock_strategy = Mock(spec=FoodCollectionStrategy)
    vendor = FoodVendor(FoodVendorType.INTER_FOOD, mock_strategy, "something", "dsfds")

    with pytest.raises(AttributeError):
        vendor.menu_url = Mock(spec=FoodCollectionStrategy)


def test_food_vendor_name_is_read_only():
    mock_strategy = Mock(spec=FoodCollectionStrategy)
    vendor = FoodVendor(FoodVendorType.INTER_FOOD, mock_strategy, "something", "dsfds")

    with pytest.raises(AttributeError):
        vendor.name = Mock(spec=FoodCollectionStrategy)


@freeze_time("2025-02-23")
def test_get_available_dates_calls_data_access_function():
    mock_session = Mock(spec=Session)
    mock_strategy = Mock(spec=TeletalStrategy)
    vendor = FoodVendor(FoodVendorType.TELETAL, mock_strategy, "something", "also something")

    mock_dates = [date(2025, 4, 14), date(2025, 4, 15)]

    with patch("food_vendors.food_vendor.get_available_dates_for_vendor", return_value=mock_dates) as mock_data_func:
        result = vendor.get_available_dates(mock_session)

    assert result == mock_dates
    mock_data_func.assert_called_once()
    called_args = mock_data_func.call_args[0]
    assert called_args[0] == mock_session
    assert called_args[1] == date(2025, 2, 23)
    assert called_args[2] == FoodVendorType.TELETAL
