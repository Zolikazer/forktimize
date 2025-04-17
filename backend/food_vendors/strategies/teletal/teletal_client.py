from urllib.parse import urlencode

import requests
from requests import Session

from monitoring.logging import JOB_LOGGER
from settings import SETTINGS


class TeletalClient:
    def __init__(self, teletal_menu_url: str = SETTINGS.teletal_menu_url,
                 teletal_ajax_url: str = SETTINGS.teletal_ajax_url,
                 timeout: int = SETTINGS.FETCHING_TIMEOUT,
                 headers: dict[str, str] = SETTINGS.HEADERS, ):
        self._teletal_menu_url: str = teletal_menu_url
        self._teletal_ajax: str = teletal_ajax_url
        self._timeout: int = timeout
        self._session: Session = requests.Session()
        self._headers: dict[str, str] = headers

    def get_main_menu(self, week: int) -> str:
        JOB_LOGGER.info("Fetching main menu html")
        response = self._session.get(f"{self._teletal_menu_url}/{week}", headers=self._headers)
        response.raise_for_status()

        return response.text

    def get_dynamic_category(self, year: int, week: int, ewid: int, varname: str) -> str:
        params = {
            "ev": year,
            "het": week,
            "ewid": ewid,
            "varname": varname,
        }
        full_url = f"{self._teletal_ajax}/szekcio?{urlencode(params)}"

        JOB_LOGGER.info(f"🌐 Fetching dynamic section: {full_url}")
        response = self._session.get(full_url, headers=self._headers, timeout=self._timeout)
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
        full_url = f"{self._teletal_ajax}/kodinfo?{urlencode(params)}"

        JOB_LOGGER.info(f"🌐 Fetching food data: {full_url}")
        response = self._session.get(full_url, headers=self._headers, timeout=self._timeout)
        response.raise_for_status()

        return response.text
