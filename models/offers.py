from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Tuple, Optional

class Location(BaseModel):
    location_name: str
    coordinates: Tuple[float, float]
    number_of_pickups: int
    number_of_drop_offs: int

class Offer(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    origin: Location
    destination: Location
    plate_number:str
    available_seats:int
    leaving_at_least: datetime
    leaving_at_last: datetime
    arrival_at_least: datetime
    arrival_at_last: datetime
    vias: List[Optional[Location]]
    message: str
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "origin": self.origin.dict(),
            "destination": self.destination.dict(),
            "plate_number": self.plate_number,
            "leaving_at_least": self.leaving_at_least,
            "leaving_at_last": self.leaving_at_last,
            "arrival_at_least": self.arrival_at_least,
            "arrival_at_last": self.arrival_at_last,
            "vias": [via.dict() if via else None for via in self.vias],
            "created_at": self.created_at
        }

