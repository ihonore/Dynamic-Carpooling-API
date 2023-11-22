from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class DemandStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Demand(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    origin: str
    destination: str
    departure_time: datetime
    arrival_time: datetime
    message: str
    status: DemandStatus
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "origin": self.origin,
            "destination": self.destination,
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at
        }

