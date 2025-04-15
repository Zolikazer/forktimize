from urllib.parse import urlencode

import requests

from monitoring.logging import JOB_LOGGER
from settings import SETTINGS


class TeletalClient:
    def __init__(self, teletal_menu_url: str = SETTINGS.teletal_menu_url,
                 teletal_ajax_url: str = SETTINGS.teletal_ajax_url,
                 timeout: int = SETTINGS.FETCHING_TIMEOUT):
        self.teletal_menu_url = teletal_menu_url
        self.teletal_ajax = teletal_ajax_url
        self.timeout = timeout
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36"
        }

    def get_main_menu(self, week: int) -> str:
        JOB_LOGGER.info("Fetching main menu html")
        response = self.session.get(f"{self.teletal_menu_url}/{week}", headers=self.headers)
        response.raise_for_status()

        return response.text

    def get_dynamic_category(self, year: int, week: int, ewid: int, varname: str) -> str:
        params = {
            "ev": year,
            "het": week,
            "ewid": ewid,
            "varname": varname,
        }
        full_url = f"{self.teletal_ajax}/szekcio?{urlencode(params)}"

        JOB_LOGGER.info(f"🌐 Fetching dynamic section: {full_url}")
        response = self.session.get(full_url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()

        return response.text

    def fetch_food_data(self, year: int, week: int, day: int, code: str) -> str:
        params = {
            "ev": year,
            "het": week,
            "tipus": 1,
            "nap": day,
            "kod": code
        }
        full_url = f"{self.teletal_ajax}/kodinfo?{urlencode(params)}"

        JOB_LOGGER.info(f"🌐 Fetching food data: {full_url}")
        response = self.session.get(full_url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()

        return response.text
