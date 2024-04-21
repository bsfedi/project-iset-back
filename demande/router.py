
from bson import ObjectId
from fastapi import APIRouter
from secuirty import *
from demande.models import *

from database import db




demande_router = APIRouter(tags=["demande"])

@demande_router.post("/attestation",)
def signup(demande :demande_presence ):
    # Insert the new user into the database
    response = db["demande_presence"].insert_one(dict(demande))

    if response:
        return {
            "message": "demande added successfully !",
        }


@demande_router.post("/verification",)
def signup(demande :demande_verification ):
    # Insert the new user into the database
    response = db["demande_verification"].insert_one(dict(demande))

    if response:
        return {
            "message": "demande added successfully !",
        }
    
@demande_router.get("/attestation/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    response = db["demande_presence"].find({"user_id": user_id})
    for attes in response:
        attes['_id']=str(attes['_id'])
        list_attes.append(attes)
    return list_attes

@demande_router.get("/verification/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    response = db["demande_verification"].find({"user_id": user_id})
    for attes in response:
        attes['_id']=str(attes['_id'])
        list_attes.append(attes)
    return list_attes
