from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Tuple, Optional

from .itinerary import Itinerary

class Offer(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    itinerary: Itinerary
    plate_number:str
    available_seats:int
    message: str
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "itinerary": self.itinerary.model_dump(),
            "plate_number": self.plate_number,
            "message": self.message,
            "created_at": self.created_at
        }

