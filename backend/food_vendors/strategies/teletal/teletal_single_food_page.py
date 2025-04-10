from bs4 import BeautifulSoup


class TeletalSingleFoodPage:
    _PROTEIN_LABEL = "Fehérje"
    _CARB_LABEL = "Szénhidrát"
    _FAT_LABEL = "Zsír"
    _CALORIES_LABEL = "Energiatartalom"

    _LABEL_CLASS = "uk-width-1-2"
    _VALUE_CLASS = "en_adag"

    def __init__(self, food_soup: BeautifulSoup):
        self._food_soup: BeautifulSoup | None = food_soup

    def get_food_data(self) -> dict[str, str]:
        return self._parse_food_data()

    def _parse_food_data(self) -> dict[str, str]:
        name = self._extract_name()
        calories = self._extract_calories()
        protein = self._extract_protein()
        carb = self._extract_carb()
        fat = self._extract_fat()

        return {"name": name,
                "calories": calories,
                "protein": protein,
                "carb": carb,
                "fat": fat, }

    def _extract_name(self) -> str:
        return self._food_soup.find("h1", class_="uk-article-title").text.strip()

    def _extract_calories(self) -> str | None:
        for row in self._food_soup.find_all("div",
                                            class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom uk-text-bold"):
            label_div = row.find("div", class_=self._LABEL_CLASS)
            if label_div and self._CALORIES_LABEL in label_div.text:
                calories_div = row.find("span", class_=self._VALUE_CLASS)
                return calories_div.text.strip() if calories_div else None

        return None

    def _extract_protein(self) -> str | None:
        for row in self._food_soup.find_all("div",
                                            class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom uk-text-bold"):
            label_div = row.find("div", class_=self._LABEL_CLASS)
            if label_div and self._PROTEIN_LABEL in label_div.text:
                calories_div = row.find("span", class_=self._VALUE_CLASS)
                return calories_div.text.strip() if calories_div else None

        return None

    def _extract_fat(self) -> str | None:
        for row in self._food_soup.find_all("div", class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom"):
            label_div = row.find("div", class_=self._LABEL_CLASS)
            if label_div and self._FAT_LABEL in label_div.text:
                calories_div = row.find("span", class_=self._VALUE_CLASS)
                return calories_div.text.strip() if calories_div else None

        return None

    def _extract_carb(self) -> str | None:
        for row in self._food_soup.find_all("div", class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom"):
            label_div = row.find("div", class_=self._LABEL_CLASS)
            if label_div and self._CARB_LABEL in label_div.text:
                calories_div = row.find("span", class_=self._VALUE_CLASS)
                return calories_div.text.strip() if calories_div else None

        return None