import json
from datetime import datetime
from typing import List

from model.food import Food


def open_json(json_file: str) -> dict:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def save_to_json(data: dict, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_food_from_json(json_file: str) -> list[Food]:
    data = open_json(json_file)

    return serialize_food_items(data)


def serialize_food_items(data: dict) -> list[Food]:
    return [
        Food(
            food_id=item['id'],
            name=item["food"]['name'],
            calories=item['energy_portion_food_one'],
            protein=int(item['protein_portion_food_one']),
            carb=int(item['carb_portion_food_one']),
            fat=int(item['fat_portion_food_one']),
            price=item['price'],
            date=datetime.strptime(item['date'], "%Y-%m-%d").date()
        )
        for food_type in data['data'].values()
        for category in food_type['categories']
        for item in category['items']
    ]
