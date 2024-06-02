
import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException ,Form,UploadFile
from stage.models import *
from secuirty import *
from demande.models import *

from database import db
import random




stage_router = APIRouter(tags=["stage"])



@stage_router.post("/add_stage")
async def add_stage(stage :stage):
    db['stage'].insert_one(dict(stage))
    return {"message":"stage added succesfully !"}

@stage_router.post("/add_pfe_stage")
async def add_stage(stage :stage_pfe ):
    stagee = db['stage'].insert_one(dict(stage))
    return str(stagee.inserted_id)

@stage_router.post("/add_cahier_cahrge/{stage_id}")
async def add_stage(stage_id,cahier_charge :  Optional[UploadFile] = File()  ):
    print(stage_id,cahier_charge)
    if cahier_charge:
        with open(os.path.join("uploads", cahier_charge.filename), "wb") as buffer:
            buffer.write(await cahier_charge.read())

    

    update_data = {}
    print(cahier_charge.filename)
    if cahier_charge:
        update_data["justif"] = cahier_charge.filename
    db["stage"].update_one({"_id": ObjectId(stage_id)}, {"$set": {"cahier_charge": update_data["justif"]}})
    return True


@stage_router.put('/update_satge/{stage_id}')
async def update_status_pfe(stage_id,staus_satge : staus_satge):
    db["stage"].update_one({"_id": ObjectId(stage_id)}, {"$set": {
      
        "status" :  staus_satge.status,
        "commantaire":staus_satge.commantaire
        }})
    return True

@stage_router.put('/note_satge/{stage_id}')
async def update_status_pfe(stage_id,stage_note : stage_note):
    db["stage"].update_one({"_id": ObjectId(stage_id)}, {"$set": {
      
        "note" :  stage_note.note,
        }})
    return True


@stage_router.get('/get_stage_by_id/{satge_id}')
async def get_stages(satge_id):

    stage = db['stage'].find_one({"_id":ObjectId(satge_id)})
    print(stage)
    stage['_id']=str(stage['_id'])

    return stage


@stage_router.get('/generate_lettre/{satge_id}')
async def generate_lettre(satge_id):

    stage = db['stage'].find_one({"_id":ObjectId(satge_id)})
    user = db['preregistres'].find_one({"user_id":ObjectId(stage['user_id'])})
    chefdepartement = db['users'].find_one({"departement":stage['departement']})
    user['_id']=str(user['_id'])
    user['user_id']=str(user['user_id'])
    stage['_id']=str(stage['_id'])
    chefdepartement['_id']=str(chefdepartement['_id'])
    

    return {"stage":stage , "chefdepartement" :chefdepartement , "user":user}

@stage_router.get('/get_stages/{user_id}')
async def get_stages(user_id):
    all_stages =[]
    stages = db['stage'].find({"user_id":user_id})
    for stage in stages:
        stage['_id']=str(stage['_id'])
        all_stages.append(stage)
    return all_stages


@stage_router.get('/get_stages_by_departement/{user_id}')
async def get_stages(user_id):
    all_stages =[]
 
    stages = db['stage'].find()
    print(stages)
    for stage in stages:
        stage['user_id'] =db['preregistres'].find_one({"user_id":ObjectId(stage['user_id'])})['personalInfo']['first_name'] + " "+db['preregistres'].find_one({"user_id":ObjectId(stage['user_id'])})['personalInfo']['last_name']
        # stage['user_id']=

        stage['_id']=str(stage['_id'])
        all_stages.append(stage)
    return all_stages

