from bs4 import BeautifulSoup

from food_vendors.strategies.teletal.teletal_client import TeletalClient
from food_vendors.strategies.teletal.teletal_food_menu_page import TeletalFoodMenuPage
from food_vendors.strategies.teletal.teletal_single_food_page import TeletalSingleFoodPage


class TeletalFoodPage:
    def __init__(self, client: TeletalClient):
        self._client = client
        self._food_page_soup: BeautifulSoup | None = None

    def get_food_data(self, year: int, week: int, category_code: str, day: int) -> dict[str, str]:
        self._load(year=year, week=week, category_code=category_code, day=day)

        if self._is_contains_multiple_foods():
            return TeletalFoodMenuPage(self._food_page_soup).get_menu_data()
        else:
            return TeletalSingleFoodPage(self._food_page_soup).get_food_data()

    def _load(self, year: int, week: int, category_code: str, day: int):
        self._food_page_soup = BeautifulSoup(
            self._client.fetch_food_data(year=year, week=week, day=day, code=category_code), "html.parser")

    def _is_contains_multiple_foods(self) -> bool:
        h1_tags = self._food_page_soup.find_all("h1", class_="uk-article-title")
        return len(h1_tags) > 1
