# from dataclasses import Field
from datetime import datetime
from bson import ObjectId
from pydantic import BaseModel, EmailStr,Field
from enum import Enum

class UserRole(str, Enum):
    passenger = "passenger"
    driver = "driver"

class User(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    username: str
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    role: UserRole
    created_at: datetime

    def model_dump(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at,
        }
