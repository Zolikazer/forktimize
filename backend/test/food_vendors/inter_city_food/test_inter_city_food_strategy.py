from contextlib import contextmanager
from unittest.mock import patch, Mock

import pytest
from requests import Response

from food_vendors.food_vendor_type import FoodVendorType
from food_vendors.strategies.e_inter_city_food.efood_strategy import EfoodStrategy
from food_vendors.strategies.e_inter_city_food.city_food_strategy import CityFoodStrategy
from food_vendors.strategies.e_inter_city_food.inter_food_strategy import InterFoodStrategy
from jobs.file_utils import load_json
from settings import SETTINGS
from test.conftest import TEST_RESOURCES_DIR, WEEK, YEAR


@pytest.fixture
def mock_requests_post_success():
    @contextmanager
    def _mock(filename: str):
        with patch("requests.post") as mock_post:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.json.return_value = load_json(str(TEST_RESOURCES_DIR / filename))
            mock_post.return_value = mock_response
            yield mock_post

    return _mock


@pytest.mark.parametrize("strategy, response_file, expected_vendor", [
    (CityFoodStrategy(), "city-response-test.json", FoodVendorType.CITY_FOOD),
    (InterFoodStrategy(), "interfood-response-test.json", FoodVendorType.INTER_FOOD),
    (EfoodStrategy(), "efood-response-test.json", FoodVendorType.EFOOD),

])
def test_inter_city_vendor_fetch_foods_fetches_foods(mock_requests_post_success, strategy, response_file,
                                                     expected_vendor):
    with mock_requests_post_success(response_file):
        result = strategy.fetch_foods_for(2025, 10)
        assert len(result.foods) > 0, "Expected food items but got none."
        assert result.foods[0].food_vendor == expected_vendor


@pytest.mark.parametrize("strategy, expected_url, response_file", [
    (CityFoodStrategy(), SETTINGS.city_food_menu_api_url, "city-response-test.json"),
    (InterFoodStrategy(), SETTINGS.inter_food_menu_api_url, "interfood-response-test.json"),
    (EfoodStrategy(), SETTINGS.efood_food_menu_api_url, "efood-response-test.json"),
])
def test_inter_city_strategy_calls_correct_url(
        mock_requests_post_success,
        strategy,
        expected_url,
        response_file,
):
    with mock_requests_post_success(response_file) as mock_post:
        strategy.fetch_foods_for(2025, 10)

        mock_post.assert_called_once()
        actual_url = mock_post.call_args[0][0]
        assert actual_url == expected_url, f"Expected URL {expected_url}, but got {actual_url}!"

@pytest.mark.parametrize("strategy_cls, expected_vendor", [
    (CityFoodStrategy, FoodVendorType.CITY_FOOD),
    (InterFoodStrategy, FoodVendorType.INTER_FOOD),
    (EfoodStrategy, FoodVendorType.EFOOD),
])
def test_strategy_get_vendor(strategy_cls, expected_vendor):
    strategy = strategy_cls()
    assert strategy.get_vendor() == expected_vendor

@pytest.mark.parametrize("strategy_cls, expected_vendor", [
    (CityFoodStrategy, FoodVendorType.CITY_FOOD),
    (InterFoodStrategy, FoodVendorType.INTER_FOOD),
    (EfoodStrategy, FoodVendorType.EFOOD),
])
@patch("requests.post")
def test_strategy_result_contains_correct_vendor(_, strategy_cls, expected_vendor):
    result = strategy_cls().fetch_foods_for(YEAR, WEEK)
    assert result.vendor == expected_vendor


@pytest.mark.parametrize("strategy, response_file, expected_url", [
    (CityFoodStrategy(), "city-response-test.json",
     SETTINGS.CITY_FOOD_IMAGE_URL_TEMPLATE),
    (InterFoodStrategy(), "interfood-response-test.json",
     SETTINGS.INTER_FOOD_IMAGE_URL_TEMPLATE),
    (EfoodStrategy(), "efood-response-test.json",
     SETTINGS.EFOOD_FOOD_IMAGE_URL_TEMPLATE),
])
def test_get_food_image_url(strategy, response_file, expected_url: str, mock_requests_post_success):
    with mock_requests_post_success(response_file):
        result = strategy.fetch_foods_for(2025, 10)

    for food in result.foods:
        assert result.images.get(food.food_id) == expected_url.format(food_id=food.food_id)


@pytest.mark.parametrize("strategy", [
    CityFoodStrategy(),
    InterFoodStrategy(),
    EfoodStrategy(),
])
def test_maintenance_response_detection(strategy):
    """Test that maintenance response is properly detected and handled."""
    # Test maintenance response: error=false, data=[]
    maintenance_response = {"error": False, "data": []}
    assert strategy._is_maintenance_response(maintenance_response) == True
    
    # Test normal response: error=false, data=populated
    normal_response = {"error": False, "data": {"breakfast": {"categories": [{"items": [{"id": 1}]}]}}}
    assert strategy._is_maintenance_response(normal_response) == False
    
    # Test error response: error=true
    error_response = {"error": True, "data": []}
    assert strategy._is_maintenance_response(error_response) == False


@patch("requests.post")
def test_fetch_foods_handles_maintenance_mode(mock_post):
    """Test that fetch_foods_for returns empty result during maintenance."""
    # Mock maintenance response
    mock_response = Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = {"error": False, "data": []}
    mock_post.return_value = mock_response
    
    strategy = CityFoodStrategy()
    result = strategy.fetch_foods_for(2025, 10)
    
    # Should return empty result gracefully
    assert result.foods == []
    assert result.images == {}
    assert result.vendor == FoodVendorType.CITY_FOOD
    assert result.raw_data == {"error": False, "data": []}
