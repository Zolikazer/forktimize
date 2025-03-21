from model.food_log_entry import FoodLogEntry


def test_food_log_entry_from_macros_basic_case():
    entry = FoodLogEntry.from_macros(protein=100, carb=200, fat=50)

    assert entry.chicken == 400
    assert entry.sugar == 200
    assert entry.oil == 38


def test_food_log_entry_handles_zero_macros():
    entry = FoodLogEntry.from_macros(protein=0, carb=0, fat=0)

    assert entry.chicken == 0
    assert entry.sugar == 0
    assert entry.oil == 0


def test_food_log_entry_does_not_return_negative_oil():
    entry = FoodLogEntry.from_macros(protein=100, carb=100, fat=5)

    assert entry.chicken == 400
    assert entry.oil == 0
