import json
from datetime import datetime
from itertools import groupby
from typing import List, Dict, Iterable

from model.food import Food


def open_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def load_data(json_file: str) -> List[Food]:
    """Parses a JSON file and returns a list of Food objects."""
    data = open_file(json_file)

    return [
        Food(
            food_id=item['id'],
            name=item["food"]['name'],
            calories=item['energy_portion_food_one'],
            protein=int(item['protein_portion_food_one']),
            carb=int(item['carb_portion_food_one']),
            fat=int(item['fat_portion_food_one']),
            price=item['price'],
            date=datetime.strptime(item['date'], "%Y-%m-%d")
        )
        for food_type in data['data'].values()
        for category in food_type['categories']
        for item in category['items']
    ]


def categorize_foods_by_date(foods: List[Food]) -> Dict[str, List[Food]]:
    """Categorizes foods by date."""
    foods.sort(key=lambda f: f.date)
    return {date: list(group) for date, group in groupby(foods, key=lambda f: f.date.strftime("%Y-%m-%d"))}


def filter_out_food(food_blacklist: list, foods: List[Food]) -> List[Food]:
    filtered_foods = filter(lambda f: not any(k.lower() in f.name.lower() for k in food_blacklist), foods)
    return _filter_out_zero_protein(filtered_foods)


def _filter_out_zero_protein(foods: Iterable[Food]) -> List[Food]:
    return list(filter(lambda f: f.protein != 0, foods))
