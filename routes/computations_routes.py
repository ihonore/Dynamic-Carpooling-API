import json
import sys
from fastapi import HTTPException
from fastapi import APIRouter
from datetime import datetime

from config.database import demands_collection
from models.demands import Demand
from schema.demands import list_serial
from bson import ObjectId

from controllers.computations import computation

router=APIRouter()

@router.get("/")
def process():
    return computation()
