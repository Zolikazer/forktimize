from unittest.mock import MagicMock

from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_menu_page import TeletalMenuPage


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
