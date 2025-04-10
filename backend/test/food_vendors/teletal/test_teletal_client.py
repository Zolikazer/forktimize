import requests_mock

from food_vendors.strategies.teletal.teletal_client import TeletalClient


def test_get_main_menu_html():
    mock_url = "https://fake-teletal.test/menu"
    mock_html = "<html><body><h1>Test Menu</h1></body></html>"

    with requests_mock.Mocker() as m:
        m.get("https://fake-teletal.test/menu/16", text=mock_html)

        client = TeletalClient(mock_url, "something")
        html = client.get_main_menu_html(16)

        assert html == mock_html


def test_get_dynamic_category_html():
    mock_ajax_url = "https://fake-teletal.test/something"
    mock_html = "<html><div>Mocked Section</div></html>"
    year = 2025
    week = 15
    ewid = 42
    varname = "fitness"

    expected_url = f"{mock_ajax_url}/szekcio?ev={year}&het={week}&ewid={ewid}&varname={varname}"

    with requests_mock.Mocker() as m:
        m.get(expected_url, text=mock_html)

        client = TeletalClient("something", mock_ajax_url)
        html = client.get_dynamic_category_html(year, week, ewid, varname)

        assert html == mock_html
        assert m.call_count == 1


def test_fetch_food_data_with_requests_mock():
    mock_ajax_url = "https://fake-teletal.test/menu"
    expected_html = "<div>Mocked food details for F999</div>"

    year = 2025
    week = 15
    day = 1
    kod = "F999"

    full_url = f"{mock_ajax_url}/kodinfo?ev=2025&het=15&tipus=1&nap=1&kod=F999"

    with requests_mock.Mocker() as m:
        m.get(full_url, text=expected_html)

        client = TeletalClient("something", mock_ajax_url)
        result = client.fetch_food_data(year=year, week=week, day=day, code=kod)

        assert result == expected_html
        assert m.call_count == 1
