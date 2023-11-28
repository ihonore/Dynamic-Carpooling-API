from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Tuple,Optional

class Location(BaseModel):
    location_name: Optional[str]
    location_address: Optional[str]
    coordinates: Tuple[float, float]
    number_of_pickups: int
    number_of_drop_offs: int
    hour_at_least: datetime
    hour_at_last: datetime

class Itinerary(BaseModel):
    origin: Location
    destination: Location
    vias: List[Optional[Location]]