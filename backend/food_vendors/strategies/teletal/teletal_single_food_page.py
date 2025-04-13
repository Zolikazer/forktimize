from bs4 import BeautifulSoup


class TeletalSingleFoodPage:
    def __init__(self, food_soup: BeautifulSoup):
        self._food_soup: BeautifulSoup | None = food_soup

    def get_food_data(self) -> dict[str, str]:
        return self._parse_food_data()

    def _parse_food_data(self) -> dict[str, str]:
        return {"name": self._extract_name(),
                "calories": self._extract_calories(),
                "protein": self._extract_protein(),
                "carb": self._extract_carb(),
                "fat": self._extract_fat(),
                "image": self._extract_image()}

    def _extract_name(self) -> str:
        return self._food_soup.find("h1", class_="uk-article-title").text.strip()

    def _extract_calories(self) -> str | None:
        return self._extract_macro("Energiatartalom", bold=True)

    def _extract_protein(self) -> str | None:
        return self._extract_macro("Fehérje", bold=True)

    def _extract_fat(self) -> str | None:
        return self._extract_macro("Zsír")

    def _extract_carb(self) -> str | None:
        return self._extract_macro("Szénhidrát")

    def _extract_macro(self, label: str, bold: bool = False) -> str | None:
        search_class = "uk-grid-small uk-margin-remove-top uk-margin-remove-bottom"
        if bold:
            search_class += " uk-text-bold"

        for row in self._food_soup.find_all("div", class_=search_class):
            label_div = row.find("div", class_="uk-width-1-2")
            if label_div and label in label_div.text:
                value_div = row.find("span", class_="en_adag")
                return value_div.text.strip() if value_div else None

        return None

    def _extract_image(self) -> str | None:
        img_tag = self._food_soup.find("img")
        if not img_tag:
            return None

        srcset = img_tag.get("srcset")
        if not srcset:
            return None

        urls = [item.strip().split(" ")[0] for item in srcset.split(",")]

        return urls[-1] if urls else None
