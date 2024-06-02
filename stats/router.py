
import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException
from secuirty import *
from stats.models import *
from database import db




stats_router = APIRouter(tags=["stats"])




@stats_router.post('/add_annonce')
async def add_annonce(annonce:annonce):
    db['annonce'].insert_one(dict(annonce))
    return True



@stats_router.get('/annonces')
async def add_annonce():
    all_annonces =[]
    annonces=db['annonce'].find()
    for an in annonces:
        an['_id']=str(an['_id'])
        all_annonces.append(an)
    return all_annonces


@stats_router.delete('/annonce/{annonce_id}')
async def delete_annonce(annonce_id):
    db['annonce'].delete_one({"_id":ObjectId(annonce_id)})
    return True


@stats_router.get('/statistique_student/{module_id}')
async def affecter_demande(module_id: str):
    all_demande_presence_validated = []
    all_demande_presence_pending = []
    all_demande_presence = []
    all_demande_verification_validated = []
    all_demande_verification_pending = []
    all_demande_verification = []
    
    demande_presence = db["demande_presence"].find({"module_id": module_id})
    for ee in demande_presence:
        all_demande_presence.append(ee)
        if ee['status'] == 'prete':
            all_demande_presence_validated.append(ee)
        elif ee['status'] == 'pending':
            all_demande_presence_pending.append(ee)

    demande_verification = db["demande_verification"].find({"module_id": module_id})
    for dv in demande_verification:
        all_demande_verification.append(dv)
        if dv['status'] == 'validated':
            all_demande_verification_validated.append(dv)
        elif dv['status'] == 'pending':
            all_demande_verification_pending.append(dv)

    total_presence = len(all_demande_presence)
    total_verification = len(all_demande_verification)

    return {
        "all_demande_presence_validated": len(all_demande_presence_validated),
        "all_demande_presence_pending": len(all_demande_presence_pending),
        "all_demande_verification_validated": len(all_demande_verification_validated),
        "all_demande_verification_pending": len(all_demande_verification_pending),
        "percentage_presence_validated": (len(all_demande_presence_validated) / total_presence) * 100 if total_presence > 0 else 0,
        "percentage_presence_pending": (len(all_demande_presence_pending) / total_presence) * 100 if total_presence > 0 else 0,
        "percentage_verification_validated": (len(all_demande_verification_validated) / total_verification) * 100 if total_verification > 0 else 0,
        "percentage_verification_pending": (len(all_demande_verification_pending) / total_verification) * 100 if total_verification > 0 else 0
    }

    