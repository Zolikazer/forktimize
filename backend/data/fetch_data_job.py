import json
from datetime import datetime
from pathlib import Path

import requests

from settings import SETTINGS

DATA_ENDPOINT = f"{SETTINGS.CITY_FOOD_API_URL}/{SETTINGS.CITY_FOOD_API_FOOD_PATH}"
RESOURCES_DIR = Path(__file__).parent.parent.resolve() / SETTINGS.DATA_DIR
CURRENT_WEEK = datetime.now().isocalendar()[1]
CURRENT_YEAR = datetime.now().year


def fetch_and_save_weekly_json():
    """Fetch JSON data for multiple weeks from an API and save to the resources directory."""

    # Ensure the resources directory exists
    RESOURCES_DIR.mkdir(parents=True, exist_ok=True)

    for week in range(CURRENT_WEEK, CURRENT_WEEK + 4):
        try:
            response = requests.post(DATA_ENDPOINT, json=_get_request_body(CURRENT_YEAR, week), timeout=10)
            response.raise_for_status()

            data = response.json()

            filename = RESOURCES_DIR / f"city-response-week-{week}.json"

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

            print(f"✅ Week {week} data saved to {filename}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching Week {week} data: {e}")
        except json.JSONDecodeError:
            print(f"❌ Error: Week {week} API response is not valid JSON!")


def _get_request_body(year: int, week: int) -> dict:
    return {"year": str(year), "week": str(week), "calorie": {"min": 0, "max": 9000}, "carb": {"min": 0, "max": 9000},
            "protein": {"min": 0, "max": 9000}, "fat": {"min": 0, "max": 9000}, "price": {"min": 0, "max": 9000},
            "favorites": False, "last_minute": False, "seek_labels": [], "ignore_labels": [], "seek_ingredients": [],
            "ignore_ingredients": []}


if __name__ == "__main__":
    fetch_and_save_weekly_json()
