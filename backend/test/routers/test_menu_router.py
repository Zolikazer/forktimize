from pathlib import Path
from unittest import TestCase

from fastapi.testclient import TestClient
from freezegun import freeze_time

from main import app
from model.menu import Menu
from settings import SETTINGS


class TestCreateMenuEndpoint(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        SETTINGS.DATA_DIR = str(Path(__file__).parent.resolve() / "../resources")

    def test_create_menu_endpoint(self):
        menu_request = {
            "date": "2025-02-24",
            "nutritional_constraints": {
                "min_calories": 1500,
                "max_calories": 2700,
            },
            "food_blacklist": ["Lencsefőzelék"]
        }
        response = self.client.post("/menu", json=menu_request)
        self.assertEqual(response.status_code, 200)

        result = Menu(**response.json())
        self.assertEqual(5, len(result.foods))
        self.assertEqual(5800, result.total_price)
        self.assertEqual(2410, result.total_calories)
        self.assertNotIn("Lencsefőzelék vagdalttal", [food.name for food in result.foods])
        print(result)

    @freeze_time("2024-02-26")
    def test_get_available_dates(self):
        response = self.client.get("/dates")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), ["2025-02-24",
                                           "2025-02-25",
                                           "2025-02-26",
                                           "2025-02-27",
                                           "2025-02-28",
                                           "2025-03-01"])
