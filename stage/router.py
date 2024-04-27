
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



@stage_router.get('/get_stages/{user_id}')
async def get_stages(user_id):
    all_stages =[]
    stages = db['stage'].find({"user_id":user_id})
    for stage in stages:
        stage['_id']=str(stage['_id'])
        all_stages.append(stage)
    return all_stages

