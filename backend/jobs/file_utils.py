import json
from io import BytesIO
from pathlib import Path

from PIL import Image


def load_json(json_file: str) -> dict:
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data


def save_to_json(data: dict | list, path: str | Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_image(content: bytes, path: str | Path):
    with open(path, "wb") as f:
        f.write(content)


def save_file(content: str, path: str | Path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def load_file(path: str | Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_image_to_webp(content: bytes, path: str | Path, quality: int = 90):
    image_bytes = BytesIO(content)
    Image.open(image_bytes).save(path, format="WEBP", quality=quality)