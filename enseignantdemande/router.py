import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException
from secuirty import *
from enseignantdemande.models import *

from database import db




enseignantdemande_router = APIRouter(tags=["enseignant demande"])

@enseignantdemande_router.post("/enseignant_demande",)
def signup(demande :demande ):
    # Insert the new user into the database
    response = db["enseignant_demande"].insert_one(dict(demande))

    if response:
        return {
            "message": "demande added successfully !",
        }


@enseignantdemande_router.get("/enseignant_demande")
async def get_demande_attestation():
    at_demandes = []
    fp_demandes = []
    response = db["enseignant_demande"].find()
    for attes in response:
        attes['_id']=str(attes['_id'])
        if attes['type']=='AT':
            at_demandes.append(attes)
        else:
            fp_demandes.append(attes)

    return {"at_demandes":at_demandes,"fp_demandes":fp_demandes}


@enseignantdemande_router.get("/enseignants_demande/{user_id}")
async def get_demandeattestation(user_id ):
    at_demandes = []
    fp_demandes = []
    response = db["enseignant_demande"].find({"user_id":user_id})
    for attes in response:
        attes['_id']=str(attes['_id'])
        
        at_demandes.append(attes)


    return {"at_demandes":at_demandes}