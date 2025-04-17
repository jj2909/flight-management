from dataclasses import dataclass, field
from typing import Optional
from app.models.base_model import DB

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

