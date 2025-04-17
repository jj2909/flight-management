from dataclasses import dataclass
from app.models.base_model import DB

@dataclass
class Airports(DB, primary_key="code"):
    code: str
    name: str
    country: str