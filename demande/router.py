
import os
from bson import ObjectId
from fastapi import APIRouter, File, HTTPException
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

    
# @demande_router.get("/attestation/{user_id}")
# async def get_demande_attestation(user_id):
#     list_attes = []
    
#     response = db["demande_presence"].find({"user_id": user_id})
#     for attes in response:
#         attes['_id'] = str(attes['_id'])
#         enseignants_names = []
#         for i in attes['enseignants'] :
#             ens = db["users"].find_one({"_id":ObjectId (i['_id'])})
#             if ens :
#                 enseignants_names.append(ens["first_name"] +" "+ ens["last_name"])
#             else :

#                 enseignants_names.append("unknow" +" "+ "unknow")

#         attes['enseignants'] = enseignants_names
#         list_attes.append(attes)
#     return list_attes

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

@demande_router.get("/verification_by_department/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    user = db["users"].find_one({"_id":ObjectId(user_id)})
  
    response = db["demande_verification"].find({"departement":user["departement"]})
    for attes in response:
        attes['_id']=str(attes['_id'])
        if attes["enseignant"]  :
            attes["enseignant"]  = db["users"].find_one({"_id":ObjectId(attes["enseignant"] )})["first_name"] + ' '+db["users"].find_one({"_id":ObjectId(attes["enseignant"] )})["last_name"]
        else:
            pass
        list_attes.append(attes)
    return list_attes


@demande_router.get("/presence_by_department/{user_id}")
async def get_demande_attestation(user_id):
    list_attes = []
    user = db["users"].find_one({"_id":ObjectId(user_id)})
    print(user)
    response = db["demande_presence"].find({"departement":user["departement"]})
    for attes in response:
        attes['_id']=str(attes['_id'])
        # if attes["enseignant"]  :
        #     attes["enseignant"]  = db["users"].find_one({"_id":ObjectId(attes["enseignant"] )})["first_name"]
        # else:
        #     pass
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
    # if not list_attes:
    #     raise HTTPException(status_code=404, detail="No demands found for this teacher ID")
    return list_attes

@demande_router.get("/verification_by_enseignant/{enseignant_id}")
async def verification_by_enseignant(enseignant_id: str):
    list_attes = []
    # Convert enseignant_id to ObjectId
    # Query documents where enseignants array contains enseignant_object_id
    response = db["demande_verification"].find({"enseignant":  enseignant_id})
    for attes in response:

        attes['_id'] = str(attes['_id'])
        list_attes.append(attes)
    # if not list_attes:
    #     raise HTTPException(status_code=404, detail="No demands found for this teacher ID")
    return list_attes

@demande_router.put("/justif/{note}/{register_id}")
async def upload_file(note, 
                      register_id,
                      justif: Optional[UploadFile] = File(None)
       
                ):
    if justif:
        with open(os.path.join("uploads", justif.filename), "wb") as buffer:
            buffer.write(await justif.read())

    

    update_data = {}
    if justif:
        update_data["justif"] = justif.filename


    db["demande_verification"].update_one({"_id": ObjectId(register_id)}, {"$set": {"justif": update_data["justif"],       
        "new_note": note,
        "status" : "validated_by_enseignant"
        }})
    return True


@demande_router.get("/accept_note/{register_id}")
async def upload_file(
                      register_id,

       
                ):

    db["demande_verification"].update_one({"_id": ObjectId(register_id)}, {"$set": {
      
        "status" :  "validated"
        }})
    return True

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


@demande_router.get("/update_status_demande_bychef/{demande_id}")
async def update_status_demande_bychef(demande_id):
    db["demande_presence"].update_one(
            {"_id": ObjectId(demande_id)},{
                "$set": {"status":"validated_by_departement"}
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

@demande_router.get("/notvalidate_verification/{demande_id}")
async def notvalidate_verification(demande_id):
    db["demande_verification"].update_one(
        {"_id": ObjectId(demande_id)},{
            "$set": {"status":"notvalidate"}
        }
        
        )
    return {"message": "done"}


@demande_router.get("/affecter_damande/{demande_id}/{enseignant_id}")
async def affecter_damande(demande_id,enseignant_id):
    db["demande_verification"].update_one(
        {"_id": ObjectId(demande_id)},{
            "$set": {"enseignant":enseignant_id}
        }
        
        )
    return {"message":"demande  affecté"}


@demande_router.get("/stats_enseignant/{enseignant_id}")
async def affecter_damande(enseignant_id):
    all_demande_presence_validated=[]
    all_demande_presence_pending=[]
    all_demande_presence=[]
    all_demande_verification_validated=[]
    all_demande_verification_pending=[]
    all_demande_verification=[]
    demande_presence = db["demande_presence"].find({"enseignants._id": {"$in": [enseignant_id]}})
    for ee in demande_presence:
        all_demande_presence.append(ee)
        for ens in ee['enseignants']:
            if ens['_id'] == enseignant_id:
                print(ens['validated'] )
                if ens['validated'] == True or ens['validated'] == True :
                    all_demande_presence_validated.append(ens)
                else:
                    all_demande_presence_pending.append(ens)

    demande_verification = db["demande_verification"].find({"enseignant":  enseignant_id})
    for dv in demande_verification :
        all_demande_verification.append(dv)
        if dv['status']=='validated' or dv['status']=='notvalidate' :
            all_demande_verification_validated.append(dv)
        else:
            all_demande_verification_pending.append(ee)




    return  {"all_demande_presence_validated" :len(all_demande_presence_validated),
             "all_demande_presence_pending":len(all_demande_presence_pending),
             "all_demande_presence":len(all_demande_presence),
             "all_demande_verification_validated" :len(all_demande_verification_validated),
             "all_demande_verification_pending":len(all_demande_verification_pending),
             "all_demande_verification":len(all_demande_verification)}



from typing import Dict


@demande_router.get("/stats_student/{student_id}")
async def affecter_damande(student_id):
    all_demande_presence_validated = []
    all_demande_presence = []
    all_demande_verification_validated = []
    all_demande_verification = []
    presence_status_count = {}
    verification_status_count = {}
    
    demande_presence = db["demande_presence"].find({"user_id":  student_id})
    for ee in demande_presence:
        all_demande_presence.append(ee)
        status = ee['status']
        if status in ['prete', 'validated']:
            all_demande_presence_validated.append(ee)
        presence_status_count[status] = presence_status_count.get(status, 0) + 1
    
    demande_verification = db["demande_verification"].find({"user_id":  student_id})
    for dv in demande_verification:
        all_demande_verification.append(dv)
        status = dv['status']
        if status == 'validated':
            all_demande_verification_validated.append(dv)
        verification_status_count[status] = verification_status_count.get(status, 0) + 1
    
    total_presence = len(all_demande_presence)
    validated_presence = len(all_demande_presence_validated)
    total_verification = len(all_demande_verification)
    validated_verification = len(all_demande_verification_validated)
    
    presence_percentage = round((validated_presence / total_presence) * 100, 2) if total_presence != 0 else 0
    verification_percentage = round((validated_verification / total_verification) * 100, 2) if total_verification != 0 else 0
    
    presence_status_percentages = {status: round((count / total_presence) * 100, 2) for status, count in presence_status_count.items()}
    verification_status_percentages = {status: round((count / total_verification) * 100, 2) for status, count in verification_status_count.items()}
    
    # Calculate the percentage of "prete" as "validated" for presence demands
    prete_percentage = round((presence_status_count.get('prete', 0) / total_presence) * 100, 2) if total_presence != 0 else 0
    presence_status_percentages['validated'] = round(presence_status_percentages.get('validated', 0) + prete_percentage, 2)
    del presence_status_percentages['prete']
    
    return {
        "all_demande_presence_validated": len(all_demande_presence_validated),
        "all_demande_presence": total_presence,
        "presence_validation_percentage": presence_percentage,
        "presence_status_percentages": presence_status_percentages,
        "all_demande_verification_validated": len(all_demande_verification_validated),
        "all_demande_verification": total_verification,
        "verification_validation_percentage": verification_percentage,
        "verification_status_percentages": verification_status_percentages
    }


@demande_router.get('/all_stats/{category}')
async def all_stats(category):
    counte_fp = []
    count_at =[]
    count_conge =[]
    if category == 'enseignant':
        # count_conge = db['absence'].count_documents({})
        demandes = db['enseignant_demande'].find()
        for dem in demandes:
            if dem["type"]=='FP':
                counte_fp.append(dem)
            elif  dem["type"]=='AT':
                count_at.append(dem)
            else:
                count_conge.append(dem)






@demande_router.get('/stats_tuitionofficer')
async def stats_tuitionofficer():
    all_demandes_déposées = []

    # Counting processed demandes
    processed_count = db["demande_presence"].count_documents({"status": "prete"})

    # Counting unprocessed demandes
    unprocessed_count = db["demande_presence"].count_documents({"status": {"$ne": "prete"}})
    preregistres_count = db["preregistres"].count_documents({"status": {"$ne": "NOTEXIST"}})
    preregistres_traités_count = db["preregistres"].count_documents({"status": "VALIDATED"})


    return {"processed_count": processed_count, "unprocessed_count": unprocessed_count,"preregistres_count":preregistres_count,"preregistres_traites_count":preregistres_traités_count}

