from dataclasses import dataclass
from app.models.base_model import DB

@dataclass
class Aircrafts(DB, primary_key="registration"):
    registration: str
    aircraft_type: str
    aircraft_category: str
    capacity: int