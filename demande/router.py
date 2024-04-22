
from bson import ObjectId
from fastapi import APIRouter, HTTPException
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
        attes['_id'] = str(attes['_id'])
        enseignants_names = []
        for i in attes['enseignants']:
            ens = db["users"].find_one({"_id": ObjectId(i)})
            enseignants_names.append(ens["first_name"] +" "+ ens["last_name"])
        attes['enseignants'] = enseignants_names
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


@demande_router.get("/attestation")
async def get_demande_attestation():
    list_attes = []
    response = db["demande_presence"].find()
    for attes in response:
        attes['_id']=str(attes['_id'])
        list_attes.append(attes)
    return list_attes

@demande_router.get("/verification")
async def get_demande_attestation():
    list_attes = []
    response = db["demande_verification"].find()
    for attes in response:
        attes['_id']=str(attes['_id'])
        list_attes.append(attes)
    return list_attes


@demande_router.get("/attestation_by_enseignant/{enseignant_id}")
async def get_demande_attestation(enseignant_id: str):
    list_attes = []
    # Convert enseignant_id to ObjectId
    enseignant_object_id = ObjectId(enseignant_id)
    # Query documents where enseignants array contains enseignant_object_id
    response = db["demande_presence"].find({"enseignants": {"$in": [enseignant_id]}})
    for attes in response:
        attes['_id'] = str(attes['_id'])
        list_attes.append(attes)
    if not list_attes:
        raise HTTPException(status_code=404, detail="No demands found for this teacher ID")
    return list_attes

@demande_router.put("/update_status_demande/{demande_id}")
async def update_status_demande(demande_id,update_demande:update_demande):

    db["demande_presence"].update_one({"_id":ObjectId(demande_id)},{
            "$set": {
                    
                    "status": update_demande.status,        

                }
        })
    return {"message":"updated sucessuflly"}

