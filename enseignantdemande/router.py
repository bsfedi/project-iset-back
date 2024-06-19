import os
from typing import List
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


@enseignantdemande_router.post("/agent_demande",)
def signup(conge :conge ):
    # Insert the new user into the database
    response = db["enseignant_demande"].insert_one(dict(conge
    ))

    if response:
        return {
            "message": "demande added successfully !",
        }



class ScheduleItem(BaseModel):
    day: str
    sessions: List[bool]

class Module(BaseModel):
    Classe: str
    ChargeTP: float
    ChargeCI: float
    module: str

class WishForm(BaseModel):
    nom: str
    prenom: str
    added_at : Optional[datetime] = datetime.now()
    user_id :str
    status : str = "pending"
    grade: str
    modules: List[Module]
    data: List[ScheduleItem]

@enseignantdemande_router.post("/fiche_de_voeux")
def submit_wish_form(wish_form: WishForm):
    wish_form.added_at = datetime.now()
    # Insert the new form into the database
    response = db["fiche_de_voeux"].insert_one(wish_form.dict())
    if response:
        return {"message": "fiche_de_voeux added successfully!"}
    else:
        return {"message": "Error adding fiche_de_voeux"}
    


@enseignantdemande_router.get("/fiche_de_voeux/{user_id}")
def submit_wish_form(user_id):
    # Insert the new form into the database
    all_fiche_de_voeux =[]
    response = db["fiche_de_voeux"].find({"user_id":user_id})
    for res in response:
        res['_id']=str(res['_id'])
        all_fiche_de_voeux.append(res)

    return all_fiche_de_voeux



@enseignantdemande_router.get("/fiche_de_voeux_by_id/{voeux_id}")
def submit_wish_form(voeux_id):
    # Insert the new form into the database
   
    response = db["fiche_de_voeux"].find_one({"_id":ObjectId(voeux_id)})
    print(response)
    response['_id']=str(response['_id'])


    return response


@enseignantdemande_router.get("/fiche_de_voeux")
def submit_wish_form():
    # Insert the new form into the database
    all_fiches = []
    response = db["fiche_de_voeux"].find()
    for res in response:
        res['_id']=str(res['_id'])
        all_fiches.append(res)
    return all_fiches






@enseignantdemande_router.get("/enseignant_demande")
async def get_demande_attestation():
    at_demandes = []
    fp_demandes = []
    response = db["enseignant_demande"].find()
    for attes in response:
        attes['_id']=str(attes['_id'])
   
        at_demandes.append(attes)


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