from urllib.parse import urlencode

import requests

from monitoring.logging import JOB_LOGGER


class TeletalClient:
    def __init__(self, teletal_menu_url: str, timeout: int = 30):
        self.teletal_menu_url = teletal_menu_url
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    def get_main_menu_html(self) -> str:
        response = self.session.get(self.teletal_menu_url, headers=self.headers)
        response.raise_for_status()

        JOB_LOGGER.info("Fetching main menu html")
        return response.text

    def get_section_html(self, year: int, week: int, ewid: int, varname: str) -> str:
        params = {
            "ev": year,
            "het": week,
            "ewid": ewid,
            "varname": varname,
        }
        full_url = f"{self.teletal_menu_url}?{urlencode(params)}"

        JOB_LOGGER.info(f"🌐 Fetching dynamic section: {full_url}")
        response = self.session.get(full_url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()

        return response.text

    def fetch_food_data(self, year: int, week: int, day: int, kod: str) -> str:
        params = {
            "ev": year,
            "het": week,
            "tipus": 1,
            "nap": day,
            "kod": kod
        }
        full_url = f"{self.teletal_menu_url}?{urlencode(params)}"

        JOB_LOGGER.info(f"🌐 Fetching food data: {full_url}")
        response = self.session.get(full_url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()

        return response.text
