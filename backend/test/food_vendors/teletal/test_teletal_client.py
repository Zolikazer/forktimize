import pytest
import requests_mock

from food_vendors.strategies.teletal.teletal_client import TeletalClient

MOCK_MENU_URL = "https://fake-teletal.test/menu"
MOCK_AJAX_URL = "https://fake-teletal.test/ajax"


@pytest.fixture
def teletal_client():
    return TeletalClient(
        teletal_menu_url=MOCK_MENU_URL,
        teletal_ajax_url=MOCK_AJAX_URL,
    )


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_get_main_menu_html__sends_correct_request_and_returns_response(teletal_client, mock_requests):
    mock_html = "<html><body><h1>Test Menu</h1></body></html>"
    expected_url = f"{MOCK_MENU_URL}/16"
    mock_requests.get(expected_url, text=mock_html)

    html = teletal_client.get_main_menu_html(16)

    assert mock_requests.called
    assert expected_url == mock_requests.request_history[0].url
    assert html == mock_html


def test_get_dynamic_category_html__builds_correct_url_and_returns_section_html(teletal_client, mock_requests):
    mock_html = "<html><div>Mocked Section</div></html>"
    year = 2025
    week = 15
    ewid = 42
    varname = "fitness"
    expected_url = f"{MOCK_AJAX_URL}/szekcio?ev={year}&het={week}&ewid={ewid}&varname={varname}"
    mock_requests.get(expected_url, text=mock_html)

    html = teletal_client.get_dynamic_category_html(year, week, ewid, varname)

    assert mock_requests.called
    assert expected_url == mock_requests.request_history[0].url
    assert html == mock_html


def test_fetch_food_data__makes_correct_request_and_returns_food_html(teletal_client, mock_requests):
    expected_html = "<div>Mocked food details for F999</div>"
    year = 2025
    week = 15
    day = 1
    code = "F999"
    expected_url = f"{MOCK_AJAX_URL}/kodinfo?ev={year}&het={week}&tipus=1&nap={day}&kod={code}"
    mock_requests.get(expected_url, text=expected_html)

    client = TeletalClient("something", MOCK_AJAX_URL)
    result = client.fetch_food_data(year=year, week=week, day=day, code=code)

    assert mock_requests.called
    assert expected_url == mock_requests.request_history[0].url
    assert result == expected_html
