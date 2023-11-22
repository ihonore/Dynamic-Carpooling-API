from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime

class Offer(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    origin: str
    destination: str
    plate_number:str
    available_seats:int
    departure_time: datetime
    arrival_time: datetime
    message: str
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "origin": self.origin,
            "destination": self.destination,
            "plate_number": self.plate_number,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "message": self.message,
            "created_at": self.created_at
        }

