from fastapi import HTTPException
from fastapi import APIRouter
from datetime import datetime

from config.database import users_collection
from models.users import User
from schema.users import list_serial
from bson import ObjectId

router=APIRouter()

@router.get("/")
def users():
    users=list_serial(users_collection.find())
    return users


# Register User //We will implement it further
@router.post("/register")
async def register_user(user:User):
    user.created_at = datetime.utcnow()
    result=users_collection.insert_one(dict(user))
    if result.inserted_id:
        user.id = result.inserted_id
        return {"message": "User registered successfully", "user": user.model_dump()}
    else:
        raise HTTPException(status_code=500, detail="Failed to register user")

# UPDATE USER
@router.put("/{id}")
async def update_user(id: str, user: User):
    result = users_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(user)},
        return_document=True
    )
    if result:
        return {"message": "User updated successfully", "user": result}
    else:
        raise HTTPException(status_code=404, detail="User not found")