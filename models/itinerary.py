from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Tuple,Optional

class Location(BaseModel):
    location_name: Optional[str]
    location_address: Optional[str]
    coordinates: Tuple[float, float] # Long, Lat
    number_of_pickups: int
    number_of_drop_offs: int
    hour_at_least: datetime
    hour_at_last: datetime
    
    def model_dump(self):
        return {
            "location_name": self.location_name,
            "location_address": self.location_address,
            "coordinates": self.coordinates,
            "number_of_pickups": self.number_of_pickups,
            "number_of_drop_offs": self.number_of_drop_offs,
            "hour_at_least": self.hour_at_least,
            "hour_at_last": self.hour_at_last
        }


class Itinerary(BaseModel):
    origin: Location
    destination: Location
    vias: List[Optional[Location]]
    
    def model_dump(self):
        return {
            "origin": self.origin.model_dump(),
            "destination": self.destination.model_dump(),
            "vias": [via.model_dump() for via in self.vias] if self.vias else None        
        }