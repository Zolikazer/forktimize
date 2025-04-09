from sqlalchemy.orm import dynamic_loader

from food_vendors.strategies.teletal.teletal_parser import TeletalParser
from test.common import TEST_RESOURCES_DIR


def test_parse_category_codes():
    test_file = TEST_RESOURCES_DIR / "teletal-main-menu-test.html"

    with open(test_file, encoding="utf-8") as f:
        html = f.read()

    codes = TeletalParser().parse_category_codes(html)

    assert len(codes) == 14
    assert "PM" in codes
    assert "NF13" in codes


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


def test_parse_dynamic_categories():
    test_file = TEST_RESOURCES_DIR / "teletal-main-menu-test.html"

    with open(test_file, encoding="utf-8") as f:
        html = f.read()

    dynamic_categories = TeletalParser().parse_dynamic_categories(html)
    assert len(dynamic_categories) == 29
    assert {'ewid': '288021481', 'varname': 'paraszt'} in dynamic_categories
    assert {'ewid': '288021481', 'varname': 'Xixo'} in dynamic_categories
