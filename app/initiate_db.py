import json
from app.models.base_model import DB
from app.models import Aircrafts, Airports, Pilots, Flights


def load_json(path: str) -> list:
    with open(path) as f:
        return json.load(f)


def initiate() -> None:
    DB.drop_all()
    DB.intialise_all()

    models = [
        (Aircrafts, "app/data/aircrafts.json"),
        (Airports, "app/data/airports.json"),
        (Pilots, "app/data/pilots.json"),
        (Flights, "app/data/flights.json"),
    ]

    for model, path in models:
        for data in load_json(path):
            model(**data).insert()
