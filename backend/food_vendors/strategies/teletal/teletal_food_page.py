from bs4 import BeautifulSoup

from exceptions import TeletalUnavailableFoodError
from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_menu_page import TeletalFoodMenuPage
from food_vendors.strategies.teletal.teletal_single_food_page import TeletalSingleFoodPage


class TeletalFoodPage:
    def __init__(self, client: TeletalClient):
        self._client: TeletalClient = client
        self._food_page_soup: BeautifulSoup | None = None
        self._year: int | None = None
        self._week: int | None = None
        self._day: int | None = None
        self._category_code: str | None = None

    def get_food_data(self) -> dict[str, str]:
        assert self._food_page_soup is not None, "You must call load() first"
        self._check_if_food_available()

        if self._is_contains_multiple_foods():
            food_data = TeletalFoodMenuPage(self._food_page_soup).get_menu_data()
        else:
            food_data = TeletalSingleFoodPage(self._food_page_soup).get_food_data()

        food_data["code"] = self._category_code
        food_data["year"] = str(self._year)
        food_data["week"] = str(self._week)
        food_data["day"] = str(self._day)

        return food_data

    def load(self, year: int, week: int, day: int, category_code: str):
        self._year = year
        self._week = week
        self._day = day
        self._category_code = category_code

        self._food_page_soup = BeautifulSoup(
            self._client.fetch_food_data(year=year, week=week, day=day, code=category_code), "html.parser")

    def get_raw_data(self) -> str:
        return str(self._food_page_soup)

    def _is_contains_multiple_foods(self) -> bool:
        h1_tags = self._food_page_soup.find_all("h1", class_="uk-article-title")
        assert len(h1_tags) > 0, "No food names were found – expected 1 or multiple <h1> tags"

        return len(h1_tags) > 1

    def _check_if_food_available(self):
        if "Jelenleg sajnos nem érhető el információ" in self._food_page_soup.text.strip():
            raise TeletalUnavailableFoodError("❌ Info not available")
