import json
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

from model.food import Food


def open_file(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def parse_json(json_file: str) -> List[Food]:
    data = open_file(json_file)

    foods = []
    for food_type in data['data'].values():
        for category in food_type['categories']:
            for item in category['items']:
                food = Food(
                    food_id=item['id'],
                    name=item["food"]['name'],
                    kcal=item['energy_portion_food_one'],
                    protein=int(item['protein_portion_food_one']),
                    carbs=int(item['carb_portion_food_one']),
                    fat=int(item['fat_portion_food_one']),
                    price=item['price'],
                    date=datetime.strptime(item['date'], "%Y-%m-%d")
                )
                foods.append(food)

    return foods


def categorize_foods_by_date(foods: List[Food]) -> Dict[str, List[Food]]:
    categorized_foods = defaultdict(list)
    for food in foods:
        date_str = food.date.strftime("%Y-%m-%d")
        categorized_foods[date_str].append(food)
    return categorized_foods


def filter_out_food(food_names: list, foods: List[Food]) -> List[Food]:
    return filter_out_zero_protein([f for f in foods if not any(k.lower() in f.name.lower() for k in food_names)])


def filter_out_zero_protein(foods: List[Food]) -> List[Food]:
    return [f for f in foods if f.protein != 0]
