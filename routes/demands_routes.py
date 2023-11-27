import json
from fastapi import HTTPException
from fastapi import APIRouter
from datetime import datetime

from config.database import demands_collection
from models.demands import Demand
from schema.demands import list_serial
from bson import ObjectId

router=APIRouter()

@router.post("/")
async def submit_demand(demand:Demand):

    demand_dict = json.loads(demand.json())
    demand_dict["created_at"] = datetime.utcnow()
    
    result=demands_collection.insert_one(demand_dict)
    if result.inserted_id:
        demand.id = result.inserted_id
        return {"message": "The demand created successfuly", "demand": demand.model_dump()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create the demand")


@router.get("/")
def demands():
    demands=list_serial(demands_collection.find())
    return demands


# UPDATE demand
@router.put("/{id}")
async def update_demand(id: str, demand: Demand):
    result = demands_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(demand)},
        return_document=True
    )
    if result:
        return {"message": "Demand updated successfully", "demand": result}
    else:
        raise HTTPException(status_code=404, detail="Demand not found")