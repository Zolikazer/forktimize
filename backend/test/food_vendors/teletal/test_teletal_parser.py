from food_vendors.strategies.teletal.teletal_parser import TeletalParser
from test.common import TEST_RESOURCES_DIR


def test_parse_food_data():
    test_file = TEST_RESOURCES_DIR / "teletal-food-test.html"

    with open(test_file, encoding="utf-8") as f:
        html = f.read()

    food_data = TeletalParser().parse_food_data(html)
    assert food_data == {"calories": "262.1 kcal",
                         "carb": "26.2 g",
                         "fat": "11.5 g",
                         "name": "ZabKása eperöntettel, édesítőszerekkel",
                         "protein": "11.3 g"}
