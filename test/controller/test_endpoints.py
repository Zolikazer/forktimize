from unittest import TestCase

from fastapi.testclient import TestClient

from main import app
from model.menu import Menu
from settings import settings


class TestCreateMenuEndpoint(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        settings.DATA_DIR = "../resources"

    def test_create_menu_endpoint(self):
        menu_request = {
            "date": "2025-02-24",
            "nutritional_constraints": {
                "min_calories": 1500,
                "max_calories": 2700,
            }
        }
        response = self.client.post("/menu", json=menu_request)
        self.assertEqual(response.status_code, 200)

        result = Menu(**response.json())
        self.assertEqual(4, len(result.foods))
        self.assertEqual(5650, result.total_price)
        self.assertEqual(2572, result.total_calories)
        print(result)
