from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Tuple

class Offer(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    origin: Tuple[float, float]
    destination: Tuple[float, float]
    plate_number:str
    available_seats:int
    leaving_at_least: datetime
    leaving_at_last: datetime
    arrival_at_least: datetime
    arrival_at_last: datetime
    via: List[Tuple[float, float]]  # List of tuples representing points with (latitude, longitude)
    message: str
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "origin": self.origin,
            "destination": self.destination,
            "plate_number": self.plate_number,
            "leaving_at_least": self.leaving_at_least,
            "leaving_at_last": self.leaving_at_last,
            "arrival_at_least": self.arrival_at_least,
            "arrival_at_last": self.arrival_at_last,
            "via": self.via,
            "message": self.message,
            "created_at": self.created_at
        }

