from dataclasses import dataclass, field
from typing import Optional
from app.models.base_model import DB

@dataclass
class Pilots(DB, primary_key="pilot_id"):
    first_name: str
    last_name: str
    base: int = field(metadata={"foreign_key": {"table": "Airports", "column": "code"}})
    airline: str
    contact: str
    pilot_id: Optional[int] = None