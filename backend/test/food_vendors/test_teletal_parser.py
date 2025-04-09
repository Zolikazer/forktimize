from food_vendors.strategies.teletal.teletal_parser import TeletalParser
from test.common import TEST_RESOURCES_DIR


def test_find_kods():
    test_file = TEST_RESOURCES_DIR / "teletal-main-menu-test.html"

    with open(test_file, encoding="utf-8") as f:
        html = f.read()

    codes = TeletalParser().parse_kods(html)

    assert len(codes) == 14
    assert "PM" in codes
    assert "NF13" in codes


def test_parse_food_data():
    test_file = TEST_RESOURCES_DIR / "teletal-food-test.html"

    with open(test_file, encoding="utf-8") as f:
        html = f.read()

    food_data = TeletalParser().parse_food_data(html)
    assert food_data == {"name": "ZabKása eperöntettel, édesítőszerekkel",
                         "calories": 262,
                         "protein": 11,
                         "carb": 26,
                         "fat": 11}
