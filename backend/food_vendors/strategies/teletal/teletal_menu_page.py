import time

from bs4 import BeautifulSoup

from food_vendors.strategies.teletal.teletal_client import TeletalClient


class TeletalMenuPage:
    def __init__(self, client: TeletalClient, delay=0.3):
        self._client = client
        self._delay = delay
        self._menu_soup: BeautifulSoup | None = None

    def get_food_category_codes(self, year: int, week: int) -> list[str]:
        self._load_menu_page(week)
        self._load_dynamic_categories(year, week)

        return self._parse_category_codes()

    def _load_menu_page(self, week: int):
        self._menu_soup = BeautifulSoup(self._client.get_main_menu_html(week), "html.parser")

    def _load_dynamic_categories(self, year: int, week: int):
        dynamic_categories_codes = self._parse_dynamic_categories()
        for category_code in dynamic_categories_codes:
            dynamic_category_html = self._client.get_dynamic_category_html(year, week, int(category_code["ewid"]),
                                                                           category_code["varname"])
            self._append_content_to_menu_page(dynamic_category_html)
            time.sleep(self._delay)

    def _append_content_to_menu_page(self, content: str):
        soup = BeautifulSoup(content, "html.parser")
        for tag in list(soup.contents):
            self._menu_soup.body.append(tag)

    def _parse_category_codes(self) -> list[str]:
        tr_elements = self._menu_soup.find_all("tr", attrs={"kod": True})

        codes = []
        for tr in tr_elements:
            kod_value = tr["kod"]
            codes.append(kod_value)

        return codes

    def _parse_dynamic_categories(self) -> list[dict[str, str]]:
        category_sections = self._menu_soup.find_all("section", attrs={"ewid": True, "section": True})

        dynamic_categories = []
        for category_section in category_sections:
            category = {
                "ewid": category_section.get("ewid"),
                "varname": category_section.get("section"),
            }
            dynamic_categories.append(category)

        return dynamic_categories