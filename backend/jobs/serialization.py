import json
from pathlib import Path


def open_json(json_file: str) -> dict:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data


def save_to_json(data: dict | list, path: str | Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_image(content: bytes, path: str | Path):
    with open(path, "wb") as f:
        f.write(content)
