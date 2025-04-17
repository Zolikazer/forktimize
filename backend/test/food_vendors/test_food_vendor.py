import pytest
from unittest.mock import Mock

from food_vendors.food_vendor import FoodVendor
from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.food_vendor_strategy import FoodVendorStrategy

def test_food_vendor_properties():
    mock_strategy = Mock(spec=FoodVendorStrategy)
    vendor = FoodVendor(FoodVendorType.TELETAL, mock_strategy)

    assert vendor.type == FoodVendorType.TELETAL
    assert vendor.strategy is mock_strategy


def test_food_vendor_type_is_read_only():
    mock_strategy = Mock(spec=FoodVendorStrategy)
    vendor = FoodVendor(FoodVendorType.CITY_FOOD, mock_strategy)

    with pytest.raises(AttributeError):
        vendor.type = FoodVendorType.TELETAL


def test_food_vendor_strategy_is_read_only():
    mock_strategy = Mock(spec=FoodVendorStrategy)
    vendor = FoodVendor(FoodVendorType.INTER_FOOD, mock_strategy)

    with pytest.raises(AttributeError):
        vendor.strategy = Mock(spec=FoodVendorStrategy)
