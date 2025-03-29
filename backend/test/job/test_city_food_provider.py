from pathlib import Path
from unittest.mock import patch, Mock

import pytest
from requests import Response

from jobs.food_providers.city_food import CityFoodProvider
from jobs.serialization import open_json


@pytest.fixture
def mock_requests_post_success():
    with patch("requests.post") as mock_post:
        mock_response = Mock()
        mock_response.json.return_value = open_json(
            str(Path(__file__).parent.parent.resolve() / "resources/city-response-test.json"))
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        yield mock_post


@pytest.fixture
def mock_requests_post_failure():
    with patch("requests.post") as mock_post:
        mock_response = Mock(spec=Response)
        mock_response.json.return_value = "Something went wrong"
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = Exception("Mocked error!")
        mock_post.return_value = mock_response
        yield mock_post


def test_city_food_fetch_foods_result_saved_to_file(mock_requests_post_success):
    city_food_provider = CityFoodProvider()

    with patch("jobs.food_providers.city_food.save_to_json") as mock_save_to_file:
        city_food_provider.fetch_foods_for(2025, 10)
        mock_save_to_file.assert_called()


def test_city_food_fetch_foods_fetches_foods(mock_requests_post_success):
    city_food_provider = CityFoodProvider()

    with patch("jobs.food_providers.city_food.save_to_json"):
        foods = city_food_provider.fetch_foods_for(2025, 10)
        assert len(foods) > 0, "No food entries were inserted into the database!"
