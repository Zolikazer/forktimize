from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch, Mock

import pytest
from requests import Response

from jobs.food_providers.inter_city_food_provider import InterCityFoodProvider
from jobs.serialization import open_json
from model.food import FoodProvider

TEST_API_ENDPOINT = "https://fake.food.api"

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


@pytest.fixture
def mock_requests_post_failure():
    with patch("requests.post") as mock_post:
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = "Something went wrong"
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Mocked error!")
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def provider():
    return InterCityFoodProvider(TEST_API_ENDPOINT, FoodProvider.CITY_FOOD)


def test_inter_city_provider_fetch_foods_result_saved_to_file(mock_requests_post_success, provider):
    with mock_requests_post_success("city-response-test.json"):
        with patch("jobs.food_providers.inter_city_food_provider.save_to_json") as mock_save_to_file:
            provider.fetch_foods_for(2025, 10)
            mock_save_to_file.assert_called()


def test_inter_city_provider_fetch_foods_fetches_foods_cityfood_data(mock_requests_post_success, provider):
    with mock_requests_post_success("city-response-test.json"):
        with patch("jobs.food_providers.inter_city_food_provider.save_to_json"):
            foods = provider.fetch_foods_for(2025, 10)
            assert len(foods) > 0, "Expected food items but got none."


def test_inter_city_provider_fetch_foods_fetches_foods_interfood_data(mock_requests_post_success, provider):
    with mock_requests_post_success("interfood-response-test.json"):
        with patch("jobs.food_providers.inter_city_food_provider.save_to_json"):
            foods = provider.fetch_foods_for(2025, 10)
            assert len(foods) > 0, "Expected food items but got none."


def test_inter_city_provider_calls_correct_url(mock_requests_post_success, provider):
    with mock_requests_post_success("city-response-test.json") as mock_post:
        with patch("jobs.food_providers.inter_city_food_provider.save_to_json"):
            provider.fetch_foods_for(2025, 10)

            mock_post.assert_called_once()
            assert mock_post.call_args[0][0] == TEST_API_ENDPOINT, "Wrong URL was called!"


@pytest.mark.parametrize("provider_enum", [FoodProvider.CITY_FOOD, FoodProvider.INTER_FOOD])
def test_inter_city_food_get_name(provider_enum):
    prov = InterCityFoodProvider("irrelevant-url", provider_enum)
    assert prov.get_name() == provider_enum
