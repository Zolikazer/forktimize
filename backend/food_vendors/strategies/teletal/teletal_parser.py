from bs4 import BeautifulSoup


class TeletalParser:
    PROTEIN_LABEL = "Fehérje"
    CARB_LABEL = "Szénhidrát"
    FAT_LABEL = "Zsír"
    CALORIES_LABEL = "Energiatartalom"

    def parse_kods(self,html: str) -> list[str]:
        soup = BeautifulSoup(html, "html.parser")
        tr_elements = soup.find_all("tr", attrs={"kod": True})

        codes = []
        for tr in tr_elements:
            kod_value = tr["kod"]
            codes.append(kod_value)

        return codes

    def parse_food_data(self, html: str) -> dict[str, int]:
        soup = BeautifulSoup(html, "html.parser")

        name = self._extract_name(soup)
        calories = self._extract_calories(soup)
        protein = self._extract_protein(soup)
        carb = self._extract_carb(soup)
        fat = self._extract_fat(soup)

        return {"name": name,
                "calories": self._to_int(calories),
                "protein": self._to_int(protein),
                "carb": self._to_int(carb),
                "fat": self._to_int(fat), }

    def _extract_name(self, soup: BeautifulSoup):
        return soup.find("h1", class_="uk-article-title").text.strip()

    def _extract_calories(self, soup: BeautifulSoup):
        for row in soup.find_all("div", class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom uk-text-bold"):
            label_div = row.find("div", class_="uk-width-1-2")
            if label_div and self.CALORIES_LABEL in label_div.text:
                calories_div = row.find("span", class_="en_adag")
                return calories_div.text.strip() if calories_div else None

        return None

    def _extract_protein(self, soup: BeautifulSoup):
        for row in soup.find_all("div", class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom uk-text-bold"):
            label_div = row.find("div", class_="uk-width-1-2")
            if label_div and self.PROTEIN_LABEL in label_div.text:
                calories_div = row.find("span", class_="en_adag")
                return calories_div.text.strip() if calories_div else None

        return None

    def _extract_fat(self, soup: BeautifulSoup):
        for row in soup.find_all("div", class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom"):
            label_div = row.find("div", class_="uk-width-1-2")
            if label_div and self.FAT_LABEL in label_div.text:
                calories_div = row.find("span", class_="en_adag")
                return calories_div.text.strip() if calories_div else None

        return None

    def _extract_carb(self, soup: BeautifulSoup):
        for row in soup.find_all("div", class_="uk-grid-small uk-margin-remove-top uk-margin-remove-bottom"):
            label_div = row.find("div", class_="uk-width-1-2")
            if label_div and self.CARB_LABEL in label_div.text:
                calories_div = row.find("span", class_="en_adag")
                return calories_div.text.strip() if calories_div else None

        return None

    def _to_int(self, nutritional_data: str) -> int:
        return int(nutritional_data.split(".")[0])
