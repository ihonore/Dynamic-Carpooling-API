from fastapi import HTTPException
from fastapi import APIRouter
from datetime import datetime

from config.database import users_collection
from models.users import User
from schema.users import list_serial
from bson import ObjectId

router=APIRouter()

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "phone_number": user["phone_number"],
        "role": user["role"],
        "created_at": user["created_at"],
    }

@router.get("/")
def users():
    users=list_serial(users_collection.find())
    return users

# Find user by ID
@router.get("/{user_id}")
def find_user_by_id(user_id: str):
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if user:
        return {"message":"User found successfully", "user":user_helper(user)}
    else:
        return {"status_code":404, "message":"User not found"}

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