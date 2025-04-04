from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch, Mock, MagicMock

import pytest
from requests import Response

from jobs.food_providers.city_food_strategy import CityFoodStrategy
from jobs.food_providers.food_providers import FoodProvider
from jobs.food_providers.inter_food_strategy import InterFoodStrategy
from jobs.serialization import open_json
from settings import SETTINGS

TEST_JSON_PATH = Path(__file__).parent.parent.resolve() / "resources"


@pytest.fixture
def mock_requests_post_success():
    @contextmanager
    def _mock(filename: str):
        with patch("requests.post") as mock_post:
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            mock_response.json.return_value = open_json(str(TEST_JSON_PATH / filename))
            mock_post.return_value = mock_response
            yield mock_post

    return _mock


@pytest.mark.parametrize("strategy, response_file, expected_provider", [
    (CityFoodStrategy(), "city-response-test.json", FoodProvider.CITY_FOOD),
    (InterFoodStrategy(), "interfood-response-test.json", FoodProvider.INTER_FOOD),
])
def test_inter_city_provider_fetch_foods_fetches_foods(mock_requests_post_success, strategy, response_file,
                                                       expected_provider):
    with mock_requests_post_success(response_file):
        foods = strategy.fetch_foods_for(2025, 10)
        assert len(foods) > 0, "Expected food items but got none."
        assert foods[0].food_provider == expected_provider


@pytest.mark.parametrize("strategy, expected_url, response_file", [
    (CityFoodStrategy(), SETTINGS.CITY_FOOD_MENU_URL, "city-response-test.json"),
    (InterFoodStrategy(), SETTINGS.INTER_FOOD_MENU_URL, "interfood-response-test.json"),
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


@pytest.mark.parametrize("strategy_cls, expected_provider", [
    (CityFoodStrategy, FoodProvider.CITY_FOOD),
    (InterFoodStrategy, FoodProvider.INTER_FOOD),
])
def test_strategy_get_name(strategy_cls, expected_provider):
    strategy = strategy_cls()
    assert strategy.get_name() == expected_provider


@pytest.mark.parametrize("strategy, expected_url", [
    (CityFoodStrategy(), SETTINGS.CITY_FOOD_MENU_URL),
    (InterFoodStrategy(), SETTINGS.INTER_FOOD_MENU_URL),
])
@patch("jobs.food_providers.inter_city_food_strategy.requests.post")
def test_get_raw_data_fetches_and_caches(mock_post, strategy, expected_url):
    expected_response = {"data": {"mock": "value"}}

    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = expected_response
    mock_post.return_value = mock_resp

    result = strategy.get_raw_data(2025, 14)
    assert result == expected_response

    mock_post.assert_called_once_with(
        expected_url,
        json=strategy._get_request_body(2025, 14),
        timeout=10
    )

    result2 = strategy.get_raw_data(2025, 14)
    assert result2 == expected_response
    assert mock_post.call_count == 1
