import re

from bs4 import BeautifulSoup


class TeletalFoodMenuPage:
    _PROTEIN_LABEL = "Fehérje"
    _CARB_LABEL = "Szénhidrát"
    _FAT_LABEL = "Zsír"
    _CALORIES_LABEL = "Energia tartalom"

    _LABEL_CLASS = "uk-width-1-2"
    _VALUE_CLASS = "en_adag"

    def __init__(self, menu_soup: BeautifulSoup):
        self._menu_soup = menu_soup

    def get_menu_data(self) -> dict[str, str]:
        return self._parse_food_data()

    def _parse_food_data(self) -> dict[str, str]:
        name = self._extract_name()
        calories = self._extract_calories()
        protein = self._extract_macro_by_label(self._PROTEIN_LABEL)
        carb = self._extract_macro_by_label(self._CARB_LABEL)
        fat = self._extract_macro_by_label(self._FAT_LABEL)

        return {"name": name,
                "calories": calories,
                "protein": protein,
                "carb": carb,
                "fat": fat, }

    def _extract_macro_by_label(self, label: str) -> str | None:
        all_divs = self._menu_soup.find_all("div", class_="uk-width-expand")

        for div in all_divs:
            if div.text.strip() == label:
                sibling = div.find_next_sibling("div")
                return sibling.text.strip() if sibling else None

        return None

    def _extract_calories(self) -> str | None:
        divs = self._menu_soup.find_all("div", class_="uk-width-expand")

        for div in divs:
            if self._CALORIES_LABEL in div.text:
                next_bold = div.find_parent("div").find_next_sibling("div")
                return next_bold.text.strip()

        return None

    def _extract_name(self) -> str | None:
        headers = self._menu_soup.find_all("h1", class_="uk-article-title")

        if len(headers) == 0:
            return None

        food_names = [re.sub(r"\s+", " ", h.text).strip() for h in headers[1:] if h.text.strip()]

        return "\n".join(food_names)
