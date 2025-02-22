import math
from datetime import datetime

import matplotlib.pyplot as plt

from algorithm.menu_algorithms import generate_menus
from algorithm.menu_creator import Menu, filter_menus_numpy, aggregate_menus
from parser import categorize_foods_by_date, filter_out_food, parse_json


def normalize(values):
    min_val = min(values)
    max_val = max(values)
    return [(val - min_val) / (max_val - min_val) for val in values]


def plot_foods(foods):
    x = [food.kcal_per_protein for food in foods]
    y = [food.price_per_kcal for food in foods]
    names = [food.name for food in foods]

    x_normalized = normalize(x)
    y_normalized = normalize(y)

    plt.figure(figsize=(10, 6))
    plt.scatter(x_normalized, y_normalized)

    for i, name in enumerate(names):
        plt.annotate(name, (x_normalized[i], y_normalized[i]))

    plt.xlabel('kcal per protein')
    plt.ylabel('price per kcal')
    plt.title('Food Plot')
    plt.grid(True)
    plt.show()


def find_closest_foods(foods, n=10):
    def distance(food):
        return math.sqrt(food.kcal_per_protein - 4 ** 2 + food.price_per_kcal ** 2)

    sorted_foods = sorted(foods, key=distance)
    return sorted_foods[:n]


if __name__ == '__main__':
    foods = parse_json("resources/city-response-week-9.json")
    today = datetime.today().strftime("%Y-%m-%d")
    foods_of_today = categorize_foods_by_date(foods)["2025-02-28"]

    food_filter_list = ["Paradicsomsaláta", "hal", "halász", "harcsa", "tengeri", "Ecetes almapaprika", "máj",
                        "tartármártás", "Barbeque", "Ludaskása"]
    filtered_foods = filter_out_food(food_filter_list, foods_of_today)

    list_of_foods_dicts = [food.__dict__ for food in filtered_foods]

    count = 0
    menus = list()
    for menu in generate_menus(filtered_foods, 2200, 2700, 7):
        menus.append(Menu(menu))
        count += 1
        if count >= 30_000_000:
            print("...stopping early...")
            print(count)
            break

    print(count)
    stats = aggregate_menus(menus)
    filtered_menus = filter_menus_numpy(menus, stats, min_protein=200, max_fat=100, max_price=6000)
    print(filtered_menus)
    print(len(filtered_menus))

    # menu = MenuCreator(max_price=7000, min_calories=2300, max_calories=2700).second_try(list_of_foods_dicts)
    # print(menu)
    # [print(f) for f in menu.foods]

    # combinations = precompute_combinations(filtered_foods)
    # print(len(combinations))
    # print(Menu(combinations[2300]))

    # print(sorted(filtered_foods, key=lambda food: food.kcal_per_protein, reverse=False))
    # print(sorted(filtered_foods, key=lambda food: food.price_per_kcal, reverse=False))
    #
    # print(find_closest_foods(filtered_foods))
    #
    # plot_foods(find_closest_foods(filtered_foods))

    # list_of_foods_dicts = [food.__dict__ for food in filtered_foods]
    #
    # print(list_of_foods_dicts)
    # print(MenuCreator(max_price=7000, min_calories=2200, max_calories=2700).create_menu(list_of_foods_dicts))
