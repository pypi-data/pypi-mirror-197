from dataclasses import dataclass
from typing import Optional


@dataclass
class Plant:
    name: str
    icon: str


def plants() -> list[Plant]:
    return [
        Plant("Aloe Vera", "/static/examples/succulents/aloe-vera.svg"),
        Plant("Bishop's Cap", "/static/examples/succulents/bishops-cap.svg"),
        Plant("Echeveria", "/static/examples/succulents/echeveria.svg"),
        Plant("Ox Tongue", "/static/examples/succulents/ox-tongue.svg"),
        Plant("Panda Plant", "/static/examples/succulents/panda-plant.svg"),
        Plant("Zebra Plant", "/static/examples/succulents/zebra-plant.svg"),
    ]


def suggest(plant: str) -> list[Plant]:
    return [p for p in plants() if p.name.lower().startswith(plant.lower())]


def search(plant: str) -> Optional[Plant]:
    return next((p for p in plants() if p.name.lower() == plant.lower()), None)
