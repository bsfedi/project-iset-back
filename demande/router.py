
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
        for i in attes['enseignants'] :
            ens = db["users"].find_one({"_id":ObjectId (i['_id'])})
            if ens :
                enseignants_names.append(ens["first_name"] +" "+ ens["last_name"])
            else :

                enseignants_names.append("unknow" +" "+ "unknow")

        attes['enseignants'] = enseignants_names
        list_attes.append(attes)
    return list_attes

    
@demande_router.get("/attestation/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    
    response = db["demande_presence"].find({"user_id": user_id})
    for attes in response:
        attes['_id'] = str(attes['_id'])
        enseignants_names = []
        for i in attes['enseignants'] :
            ens = db["users"].find_one({"_id":ObjectId (i['_id'])})
            if ens :
                enseignants_names.append(ens["first_name"] +" "+ ens["last_name"])
            else :

                enseignants_names.append("unknow" +" "+ "unknow")

        attes['enseignants'] = enseignants_names
        list_attes.append(attes)
    return list_attes

@demande_router.get("/validated_attestation/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    
    response = db["demande_presence"].find({"user_id": user_id, "status": {"$ne": "validated_by_enseignant"}})
    for attes in response:
        attes['_id'] = str(attes['_id'])
        enseignants_names = []
        for i in attes['enseignants']:
            ens = db["users"].find_one({"_id": ObjectId(i['_id'])})
            if ens:
                enseignants_names.append(ens["first_name"] + " " + ens["last_name"])
            else:
                enseignants_names.append("unknown" + " " + "unknown")

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
    response = db["demande_presence"].find({"enseignants._id": {"$in": [enseignant_id]}})
    for attes in response:
        attes['_id'] = str(attes['_id'])
        list_attes.append(attes)
    if not list_attes:
        raise HTTPException(status_code=404, detail="No demands found for this teacher ID")
    return list_attes

@demande_router.put("/update_status_demande/{demande_id}/{enseignant_id}")
async def update_status_demande(demande_id, enseignant_id, update_demande: update_demande):

    db["demande_presence"].update_one(
        {"_id": ObjectId(demande_id), "enseignants._id": enseignant_id},
        {
            "$set": {
                "enseignants.$.validated": update_demande.validated
            }
        }
    )
    # Check if all enseignants have validated status as True
    demande = db["demande_presence"].find_one({"_id": ObjectId(demande_id)})
    all_validated = all(enseignant.get('validated', False) for enseignant in demande.get('enseignants', []))
    
    # If all enseignants have validated status as True, return "ok"
    if all_validated:
        db["demande_presence"].update_one(
        {"_id": ObjectId(demande_id)},{
            "$set": {"status":"validated_by_enseignant"}
        }
        
        )
    return {"message": "updated successfully"}


@demande_router.get("/update_new_status_demande/{demande_id}")
async def update_new_status_demande(demande_id):
    db["demande_presence"].update_one(
        {"_id": ObjectId(demande_id)},{
            "$set": {"status":"prete"}
        }
        
        )
    return {"message": "done"}