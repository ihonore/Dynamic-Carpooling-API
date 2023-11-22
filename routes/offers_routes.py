from fastapi import HTTPException
from fastapi import APIRouter
from datetime import datetime

from config.database import offers_collection
from models.offers import Offer
from schema.offers import list_serial
from bson import ObjectId

router=APIRouter()

@router.post("/")
async def submit_offer(offer:Offer):
    offer.created_at = datetime.utcnow()
    result=offers_collection.insert_one(dict(offer))
    if result.inserted_id:
        offer.id = result.inserted_id
        return {"message": "The offer created successfuly", "offer": offer.model_dump()}
    else:
        raise HTTPException(status_code=500, detail="Failed to create the offer")


@router.get("/")
def offers():
    offers=list_serial(offers_collection.find())
    return offers


@router.put("/{id}")
async def update_offer(id: str, offer: Offer):
    result = offers_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": dict(offer)},
        return_document=True
    )
    if result:
        return {"message": "Offer updated successfully", "offer": result}
    else:
        raise HTTPException(status_code=404, detail="Offer not found")