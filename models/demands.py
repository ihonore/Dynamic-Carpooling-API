from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import List, Tuple,Optional

from .itinerary import Itinerary

class DemandStatus(str, Enum):
    initialized = "initialized"
    validated = "validated"
    pending = "pending"
    preposition = "preposition"
    accepted = "accepted"
    resubmission_pending = "resubmission_pending"
    refused = "refused"

class Demand(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    user_id: str
    itinerary: Itinerary
    passengers_number:int
    message: str
    status: DemandStatus
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "user_id": self.user_id,
            "itinerary": self.itinerary.dict(),
            "passengers_number":self.passengers_number,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at
        }
