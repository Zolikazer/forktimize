from unittest.mock import MagicMock

from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage
from test.common import TEST_RESOURCES_DIR


def test_get_food_category_codes():
    fake_menu_html = """
    <html><body>
        <tr kod="HU">
        <section ewid="123" section="Hidegkonyha" ev="2025" het="15"></section>
    </body></html>
    """

    fake_dynamic_category = '<tr kod="ZK"></tr><tr kod="LE"></tr>'

    mock_client = MagicMock(spec=TeletalClient)
    mock_client.get_main_menu_html.return_value = fake_menu_html
    mock_client.get_dynamic_category_html.return_value = fake_dynamic_category

    page = TeletalMenuPage(client=mock_client, delay=0)
    codes = page.get_food_category_codes(year=2025, week=15)

    assert codes == ["HU", "ZK", "LE"]
    mock_client.get_main_menu_html.assert_called_once()
    mock_client.get_dynamic_category_html.assert_called_once_with(2025, 15, 123, "Hidegkonyha")

def test_menu_page_get_price_returns_price():
    test_file = TEST_RESOURCES_DIR / "teletal-main-menu-test.html"
    mock_client = MagicMock(spec=TeletalClient)

    with open(test_file, encoding="utf-8") as f:
        test_menu_page = f.read()

    mock_client.get_main_menu_html.return_value = test_menu_page
    mock_client.get_dynamic_category_html.return_value = ""

    menu_page = TeletalMenuPage(client=mock_client, delay=0)
    menu_page.load(15)

    assert menu_page.get_price("RE1", 1) == "295 Ft"
    assert menu_page.get_price("RE2", 5) == "385 Ft"
    assert menu_page.get_price("C", 1) == "1.890 Ft"




