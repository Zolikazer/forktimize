import pytest

from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from jobs.file_utils import load_file
from test.conftest import YEAR, WEEK, TEST_RESOURCES_DIR


def test_get_food_category_codes__returns_static_and_dynamic_codes(mock_teletal_client):
    ewid = 123
    category = "Hidegkonyha"
    menu_html = f"""
    <html><body>
        <tr kod="HU">
        <section ewid="{ewid}" section={category} ev={YEAR} het={WEEK}></section>
    </body></html>
    """

    fake_dynamic_category = '<tr kod="ZK"></tr><tr kod="LE"></tr>'
    teletal_client = mock_teletal_client(get_main_menu=menu_html, get_dynamic_category=fake_dynamic_category)

    page = TeletalMenuPage(client=teletal_client, delay=0)
    page.load(week=WEEK)
    codes = page.get_food_category_codes()

    assert codes == {"HU", "ZK", "LE"}
    teletal_client.get_main_menu.assert_called_once()
    teletal_client.get_dynamic_category.assert_called_once_with(YEAR, WEEK, ewid, category)


@pytest.mark.parametrize("code, day, expected", [
    ("RE1", 1, "295 Ft"),
    ("RE2", 5, "385 Ft"),
    ("C", 1, "1.890 Ft"),
])
def test_get_price__returns_price_from_regular_layout(mock_teletal_client, code, day, expected):
    menu_html = load_file(TEST_RESOURCES_DIR / "teletal-main-menu-test.html")
    teletal_client = mock_teletal_client(get_main_menu=menu_html)

    menu_page = TeletalMenuPage(client=teletal_client, delay=0)
    menu_page.load(15)

    assert menu_page.get_price(code, day) == expected


def test_get_price__returns_price_from_menu_style_layout(mock_teletal_client):
    menu_html = load_file(TEST_RESOURCES_DIR / "teletal-menu-style-category-test.html")
    teletal_client = mock_teletal_client(get_main_menu=menu_html)

    menu_page = TeletalMenuPage(client=teletal_client, delay=0)
    menu_page.load(15)

    assert menu_page.get_price("Z10", 1) == "3.640 Ft"
    assert menu_page.get_price("Z10", 5) == "3.640 Ft"


def test_get_food_category_codes__raises_if_called_before_load(mock_teletal_client):
    page = TeletalMenuPage(mock_teletal_client())

    with pytest.raises(AssertionError, match="You must call load\\(\\) first"):
        page.get_food_category_codes()


def test_get_price__returns_none_when_price_not_found(mock_teletal_client):
    menu_html = "<html><body></body></html>"
    teletal_client = mock_teletal_client(get_main_menu=menu_html)

    menu_page = TeletalMenuPage(teletal_client)
    menu_page.load(15)

    assert menu_page.get_price("NON_EXISTENT", 1) is None


def test_menu_page_load__calls_client_with_correct_week(mock_teletal_client):
    ewid = 123
    category = "Hidegkonyha"
    menu_html = f"""
    <html><body>
        <tr kod="HU">
        <section ewid="{ewid}" section={category} ev={YEAR} het={WEEK}></section>
    </body></html>
    """
    client = mock_teletal_client(get_main_menu=menu_html)

    page = TeletalMenuPage(client)
    page.load(week=WEEK)

    client.get_main_menu.assert_called_once_with(WEEK)
    client.get_dynamic_category.assert_called_once_with(YEAR, WEEK, ewid, category)
