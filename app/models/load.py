from typing import Optional
import json
from app.models.base_model import DB
from dataclasses import dataclass, field


@dataclass
class Aircrafts(DB, primary_key="registration"):
    registration: str
    aircraft_type: str
    aircraft_category: str
    age: int
    capacity: int


@dataclass
class Airports(DB, primary_key="code"):
    code: str
    name: str
    country: str


@dataclass
class Pilots(DB, primary_key="pilot_id"):
    first_name: str
    last_name: str
    base: int = field(metadata={"foreign_key": {"table": "Airports", "column": "code"}})
    airline: str
    contact: str
    pilot_id: Optional[int] = None


@dataclass
class Flights(DB, primary_key="flight_id"):
    departure_time: str
    arrival_time: str
    pilot_id: int = field(
        metadata={"foreign_key": {"table": "Pilots", "column": "pilot_id"}}
    )
    departure_id: str = field(
        metadata={
            "foreign_key": {
                "table": "Airports",
                "column": "code",
                "alias": "DepartureAirport",
            }
        }
    )
    destination_id: str = field(
        metadata={
            "foreign_key": {
                "table": "Airports",
                "column": "code",
                "alias": "DestinationAirport",
            }
        }
    )
    aircraft_id: str = field(
        metadata={"foreign_key": {"table": "Aircrafts", "column": "registration"}}
    )
    flight_id: Optional[int] = None


# if __name__ == "__main__":


def initiate() -> None:
    DB.drop_all()
    DB.intialise_all()

    with open("app/data/aircrafts.json") as f:
        aircraft_data = json.load(f)
    [Aircrafts(**data).insert() for data in aircraft_data]

    with open("app/data/airports.json") as f:
        airport_data = json.load(f)
    [Airports(**data).insert() for data in airport_data]

    with open("app/data/pilots.json") as f:
        pilot_data = json.load(f)
    [Pilots(**data).insert() for data in pilot_data]

    with open("app/data/flights.json") as f:
        flight_data = json.load(f)
    [Flights(**data).insert() for data in flight_data]
